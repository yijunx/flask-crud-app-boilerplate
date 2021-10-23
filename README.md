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

# Authorization (casbin)
* for specific resources `p, user_id, resource_id, right1 | right2 | right3 ...`
* actions are `action1, action2, action3..` etc, can be very flexible
* now we need a mapping and a function to do the match. This `resource_right_action_mapping` is created at flask app starting, which means we can easily change the user's right of certain actions, without updating the database! (because in database there are only rights, there is no actions allowed based on the right given to a user or role)! `resource_right_action_mapping` is a dictionary of sets.
    
        resource_right_action_mapping = {
            "right1": {"action1", "action2"},
            "right2": {"action1", "action2", "action3"},
            "right3": {"action1", "action2", "action5", "action5"}
        }

        def actions_mapping(action: str, resource_right: str) -> bool:
            """
            actions are get download patch share. They are from requests.
            resource_right are own / edit / view, They are from policies.
            """
            if resource_right in resource_right_action_mapping:
                if action in resource_right_action_mapping[resource_right]:
                    return True
            return False

        casbin_enforcer.add_function("actions_mapping", actions_mapping)

* above methods solves for the specific resource for user group
* now lets think about the admin group, first need to have a admin role id: `g, user_id_for_user_1, admin_role_1_id`. This indicates user_1 is an admin in the with the role `admin_role_1_id`
* then we can add policies for admin role: `p, admin_role_1_id, admin_resource, admin_role_1_right`. **This policies will need to be there from the beginning (before flask starts, so it can be added via initContainers to seed the database, or use some flask functions before app starts)**. And since we have admin rights, we need to update the resource_right_action_mapping.

        resource_right_action_mapping = {
            "right1": {"action1", "action2"},
            "right2": {"action1", "action2", "action3"},
            "right3": {"action1", "action2", "action5", "action5"},
            "admin_role_1_right": {"admin_action1", "admin_action2", "action1"}  # maybe we can take out actionX here if we dont want admin to have such action allowed!!
        }
        # and of course we can have admin_role_2_right...

* then in `enforcer.enforce(admin_user.id, admin_resource, admin_action1)` will allow. The format aligns with `enforcer.enforce(normal_user.id, normal_specific_resource(items/<item_id>), delete)`
* now we need to let admin_users can do any operations on any resource, we can add an object mapping functions

        def objects_mapping(object_from_request: str, object_from_policy: str):
            """
            admin users will have * in obj in the admin role policy, so admin user can
            do things on any resource
            """
            if object_from_policy == "*":
                return True
            else:
                return object_from_request == object_from_policy

* finally, the `model.conf`

        [request_definition]
        r = sub, obj, act

        [policy_definition]
        p = sub, obj, act

        [role_definition]
        g = _, _

        [policy_effect]
        e = some(where (p.eft == allow))

        [matchers]
        m = g(r.sub, p.sub) && (objects_mapping(r.obj, p.obj)) && (actions_mapping(r.act, p.act))



