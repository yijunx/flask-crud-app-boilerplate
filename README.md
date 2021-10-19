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
* groups decides
  * ADMIN group, can get all resources as it has admin rights
  * USER group, can only get resources he/she has access to
* specific resource decides
  * there are actions like get/patch/delete/share/unshare
    * own -> get/patch/delete/share/unshare (everything)
    * edit -> get/patch
    * view -> get
  * when a resource is created, the owner gets them all, owner has the right to `own`
  * the owner can share this to another user, another user has the right to `view` or `edit`
