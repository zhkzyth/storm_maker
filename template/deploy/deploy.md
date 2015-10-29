# readme
talk about deploy stuff

## what

- strategy
  - use [virtualenv][1] to offer solo env for running app in a clean context
  - use [supervisor][2] to control multi tornado processes
  - use [nginx][3] to offer load balance

- auto release scripts
  - either [ansible][4] or [fabric][5] is ok
  - at this project we use fabric

## how
- configure the `server.supervisord` and `project.supervisord` files.

- choose the env, that say, you want to deploy to dev server.
then we run below command `fab dev deploy`.

## ref
- [Tornado + Supervisord + Nginx configuration](http://gracece.net/2014/03/Tornado-supervisor+nginx/)
- [tornado official deploy docs](http://www.tornadoweb.org/en/stable/overview.html?highlight=nginx)
- [Ansible official docs](http://docs.ansible.com/index.html)
- [Ansible crash course](http://tomoconnor.eu/blogish/getting-started-ansible/#.U3cd5i918y4)

## tips
- todo

[1]: https://virtualenv.readthedocs.org/en/latest/
[2]: http://supervisord.org/
[3]: https://www.nginx.com/
[4]: http://www.ansible.com/
[5]: http://www.fabfile.org/
