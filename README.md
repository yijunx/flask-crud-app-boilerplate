# flask-crud-app-boilerplate
a bash script to create basic flask project with devcontainers, Dockerfile and various stuff

# How to bring it up
* requires postgres to be up, the repo of the infra setting is at https://github.com/yijunx/localhost-dev-infra
* open this repo in the vscode devcontainer then `make up`

# How to run tests
* `make test`

# Why create repository codes for casbin (add policy, group etc)
* can keep track of created by and created at
* can use sqlalchmy to directly pull out who can access what, and what can be accessed by who
* we will add an comparison for it...

# RBAC
* for specific resources `p, user_id, resource_id, right1 | right2 | right3 ...`
* actions are `action1, action2, action3..` etc, can be very flexible
* now we need a function to do the match
    
    resource_right_action_mapping = {
        "right1": {"action1", "action2"},
        "right2": {"action1", "action2", "action3"},
        "right3": {"action1", "action2", "action5", "action5"}
    }

    def actions_mapping(action: str, resource_right: str) -> bool:
        """
        actions are get download patch share...
        resource_right are own / edit / view
        """
        if resource_right in resource_right_action_mapping:
            if action in resource_right_action_mapping[resource_right]:
                return True
        return False

    casbin_enforcer.add_function("actions_mapping", actions_mapping)

* above methods solves for the specific resource for user group
* now lets think about the admin group, first need to have a admin role id: `g, user_id_for_user_1, admin_role_id`. This indicates user_1 is an admin
* then we can add policies for admin role: `p, admin_role_id, admin_resource, admin_action`
* then in `enforcer.enforce(admin_user.id, admin_resource, admin_action)` will allow. The format aligns with `enforcer.enforce(normal_user.id, normal_specific_resource(items/<item_id>), delete)`
