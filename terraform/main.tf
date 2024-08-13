terraform {
  required_providers {
    permitio = {
      source  = "registry.terraform.io/permitio/permit-io"
      version = "~> 0.0.1"
    }
  }
}

variable "permit_api_key" {
  type = string
}


provider "permitio" {
    api_url = "https://api.permit.io"
    api_key = var.permit_api_key
}

resource "permitio_resource" "design" {
  key         = "design"
  name        = "Designs"
  description = "A ui design"
  actions     = {
    "create" = { 
        "name" = "create",
        "description" = "create a design"
    },
    "view" = {
        "name" = "view",
        "description" = "view a design",
    },
    "edit" = {
        "name" = "edit",
        "description" = "edit a design"
    },
    "delete" = {
        "name" = "delete",
        "description" = "delete a design",
    }
  }
  attributes = {
    "creator" = {
        "description" = "The user who created the design"
        "type" = "string"
    }
  }
}

resource "permitio_resource_set" "own_design" {
  key        = "own_design"
  name       = "Own Designs"
  resource   = permitio_resource.design.key
  conditions = jsonencode({
    "allOf" : [
      {
        "allOf" : [
          { "resource.creator" : { "equals" : { "ref" : "user.key" } } },
        ],
      },
    ],
  })
  depends_on = [
    permitio_resource.design,
  ]
}

resource "permitio_resource" "comment" {
  key     = "comment"
  name    = "Comments"
  actions = {
    "create" = { "name" = "create" }
    "edit" = { "name" = "edit" }
    "delete" = { "name" = "delete" }
  }
  attributes = {
    "author" = {
      "description" = "The user key who created the comment",
      "type"        = "string"
    }
  }
}

resource "permitio_resource_set" "own_comment" {
  key        = "own_comment"
  name       = "Own Comments"
  resource   = permitio_resource.comment.key
  conditions = jsonencode({
    "allOf" : [
      {
        "allOf" : [
          { "resource.author" : { "equals" : { "ref" : "user.key" } } },
        ],
      },
    ],
  })
  depends_on = [
    permitio_resource.comment,
  ]
}

// Rebac Role blocks.

resource "permitio_relation" "design_comment_relation" {
  key              = "parent"
  name             = "Design parent of Comment"
  subject_resource = permitio_resource.design.key
  object_resource  = permitio_resource.comment.key
  depends_on       = [
    permitio_resource.design,
    permitio_resource.comment,
  ]
}

resource "permitio_role" "design_creator" {
  key         = "creator"
  name        = "creator"
  description = "edit and delete own designs"
  resource    = permitio_resource.design.key
  permissions = ["edit", "delete"]
  depends_on  = [
    permitio_resource.design
  ]
}

resource "permitio_role" "comment_moderator" {
  key         = "moderator"
  name        = "moderator"
  description = "Delete comments on own designs"
  resource    = permitio_resource.comment.key
  permissions = ["delete"]
  depends_on  = [
    permitio_resource.comment
  ]
}

// Derive design#creator to comment#moderator for child comments
resource "permitio_role_derivation" "design_creator_comment_moderator" {
  role        = permitio_role.design_creator.key
  on_resource = permitio_resource.design.key
  resource    = permitio_resource.comment.key
  to_role     = permitio_role.comment_moderator.key
  linked_by   = permitio_relation.design_comment_relation.key
  depends_on  = [
    permitio_resource.design,
    permitio_resource.comment,
    permitio_role.comment_moderator,
    permitio_role.design_creator,
    permitio_relation.design_comment_relation,
  ]
}

resource "permitio_role" "viewer" {
  key         = "viewer"
  name        = "viewer"
  description = "view and comment on all designs"
  permissions = ["design:view", "comment:create"]
  depends_on  = [
    permitio_resource.design,
    permitio_resource.comment,
  ]
}

resource "permitio_role" "creator" {
  key         = "creator"
  name        = "creator"
  description = "Create designs, edit and delete them, and delete comments on them"
  permissions = ["design:view", "design:create"]
  depends_on  = [
    permitio_resource.design,
  ]
}

resource "permitio_role" "admin" {
  key         = "admin"
  name        = "admin"
  description = "Delete any design or comment"
  permissions = ["design:create", "design:view", "design:edit", "design:delete", "comment:create", "comment:edit", "comment:delete"]
  depends_on  = [
    permitio_resource.design,
    permitio_resource.comment,
  ]
}

// Give 'editor' role permissions to 'own_design:edit'
resource "permitio_condition_set_rule" "allow_editors_to_edit_own_designs" {
  user_set     = permitio_role.creator.key
  resource_set = permitio_resource_set.own_design.key
  permission   = "design:edit"
  depends_on   = [
    permitio_resource_set.own_design,
  ]
}

// Give 'editor' role permissions to 'own_design:delete'
resource "permitio_condition_set_rule" "allow_editors_to_delete_own_designs" {
  user_set     = permitio_role.creator.key
  resource_set = permitio_resource_set.own_design.key
  permission   = "design:delete"
  depends_on   = [
    permitio_resource_set.own_design,
  ]
}

// Give 'viewer' role permissions to 'own_comment:edit'
resource "permitio_condition_set_rule" "allow_viewers_to_edit_own_comments" {
  user_set     = permitio_role.viewer.key
  resource_set = permitio_resource_set.own_comment.key
  permission   = "comment:edit"
  depends_on   = [
    permitio_resource_set.own_comment,
  ]
}

// Give 'viewer' role permissions to 'own_comment:delete'
resource "permitio_condition_set_rule" "allow_viewers_to_delete_own_comments" {
  user_set     = permitio_role.viewer.key
  resource_set = permitio_resource_set.own_comment.key
  permission   = "comment:delete"
  depends_on   = [
    permitio_resource_set.own_comment,
  ]
}



