from __future__ import annotations

import os
import os.path
from glob import glob

import click
import pkg_resources
from tutor import hooks

from .__about__ import __version__

########################################
# CONFIGURATION
########################################

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        # Add your new settings that have default values here.
        # Each new setting is a pair: (setting_name, default_value).
        # Prefix your setting names with 'ONTASK_'.
        ("ONTASK_VERSION", __version__),
        ("ONTASK_HOST", "ontask.{{ LMS_HOST }}"),
        ("ONTASK_PORT", 8080),
        ("ONTASK_DB_NAME", "ontask"),
        ("ONTASK_DB_USER", "ontask"),
        ("ONTASK_POSTGRES_HOST", "postgres"),
        ("ONTASK_DOCKER_IMAGE", "docker.io/edunext/ontask:0.3.0"),
        ("ONTASK_POSTGRES_DOCKER_IMAGE", "postgres:14.12-bullseye"),
        ("ONTASK_DATABASE_URL", "postgres://{{ ONTASK_DB_USER }}:{{ ONTASK_POSTGRES_PASSWORD }}@postgres:5432/{{ ONTASK_DB_NAME }}"),
        ("ONTASK_REDIS_URL", "redis://{{ REDIS_HOST }}:{{ REDIS_PORT }}"),
        ("ONTASK_APP_VERSION", "Version_11_1"),
        ("ONTASK_EXTRA_PRODUCTION_SETTINGS", ""),
        ("ONTASK_EXTRA_DEV_SETTINGS", ""),
        ("RUN_ONTASK", True),
        ("RUN_POSTGRES", True),
    ]
)

hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        # Add settings that don't have a reasonable default for all users here.
        # For instance: passwords, secret keys, etc.
        # Each new setting is a pair: (setting_name, unique_generated_value).
        # Prefix your setting names with 'ONTASK_'.
        # For example:
        ("ONTASK_SECRET_KEY", "{{ 24|random_string }}"),
        ("ONTASK_POSTGRES_PASSWORD", "{{ 8|random_string }}"),
        ("ONTASK_SUPERUSER_NAME", "admin"),
        ("ONTASK_SUPERUSER_EMAIL", "admin@mail.com"),
        ("ONTASK_SUPERUSER_PWD", "{{ 24|random_string }}"),
        ("ONTASK_EMAIL_ACTION_NOTIFICATION_SENDER", "admin@mail.com"),
        ("ONTASK_POSTGRES_ROOT_USERNAME", "postgres"),
        ("ONTASK_POSTGRES_ROOT_PASSWORD", "{{ 8|random_string }}"),
    ]
)

hooks.Filters.CONFIG_OVERRIDES.add_items(
    [
        # Danger zone!
        # Add values to override settings from Tutor core or other plugins here.
        # Each override is a pair: (setting_name, new_value). For example:
        ### ("PLATFORM_NAME", "My platform"),
    ]
)


########################################
# INITIALIZATION TASKS
########################################

# To add a custom initialization task, create a bash script template under:
# tutorontask/templates/ontask/jobs/init/
# and then add it to the MY_INIT_TASKS list. Each task is in the format:
# ("<service>", ("<path>", "<to>", "<script>", "<template>"))
MY_INIT_TASKS: list[tuple[str, tuple[str, ...]]] = [
    # For example, to add LMS initialization steps, you could add the script template at:
    # tutorontask/templates/ontask/jobs/init/lms.sh
    # And then add the line:
    ### ("lms", ("ontask", "jobs", "init", "lms.sh")),
    ("postgres", ("ontask", "jobs", "init", "postgres", "init.sh")),
    ("ontask", ("ontask", "jobs", "init", "ontask", "init.sh")),
]


# For each task added to MY_INIT_TASKS, we load the task template
# and add it to the CLI_DO_INIT_TASKS filter, which tells Tutor to
# run it as part of the `init` job.
for service, template_path in MY_INIT_TASKS:
    full_path: str = pkg_resources.resource_filename(
        "tutorontask", os.path.join("templates", *template_path)
    )
    with open(full_path, encoding="utf-8") as init_task_file:
        init_task: str = init_task_file.read()
    hooks.Filters.CLI_DO_INIT_TASKS.add_item((service, init_task))


########################################
# DOCKER IMAGE MANAGEMENT
########################################


# Images to be built by `tutor images build`.
# Each item is a quadruple in the form:
#     ("<tutor_image_name>", ("path", "to", "build", "dir"), "<docker_image_tag>", "<build_args>")
hooks.Filters.IMAGES_BUILD.add_items(
    [
        # To build `myimage` with `tutor images build myimage`,
        # you would add a Dockerfile to templates/ontask/build/myimage,
        # and then write:
        ### (
        ###     "myimage",
        ###     ("plugins", "ontask", "build", "myimage"),
        ###     "docker.io/myimage:{{ ONTASK_VERSION }}",
        ###     (),
        ### ),
        (
            "ontask",
            ("plugins", "ontask", "build", "ontask"),
            "{{ ONTASK_DOCKER_IMAGE }}",
            (),
        ),
    ]
)


# Images to be pulled as part of `tutor images pull`.
# Each item is a pair in the form:
#     ("<tutor_image_name>", "<docker_image_tag>")
hooks.Filters.IMAGES_PULL.add_items(
    [
        # To pull `myimage` with `tutor images pull myimage`, you would write:
        ### (
        ###     "myimage",
        ###     "docker.io/myimage:{{ ONTASK_VERSION }}",
        ### ),
        (
            "ontask",
            "{{ ONTASK_DOCKER_IMAGE }}",
        ),
    ]
)


# Images to be pushed as part of `tutor images push`.
# Each item is a pair in the form:
#     ("<tutor_image_name>", "<docker_image_tag>")
hooks.Filters.IMAGES_PUSH.add_items(
    [
        # To push `myimage` with `tutor images push myimage`, you would write:
        ### (
        ###     "myimage",
        ###     "docker.io/myimage:{{ ONTASK_VERSION }}",
        ### ),
        (
            "ontask",
            "{{ ONTASK_DOCKER_IMAGE }}",
        ),
    ]
)


########################################
# TEMPLATE RENDERING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

hooks.Filters.ENV_TEMPLATE_ROOTS.add_items(
    # Root paths for template files, relative to the project root.
    [
        pkg_resources.resource_filename("tutorontask", "templates"),
    ]
)

hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    # For each pair (source_path, destination_path):
    # templates at ``source_path`` (relative to your ENV_TEMPLATE_ROOTS) will be
    # rendered to ``source_path/destination_path`` (relative to your Tutor environment).
    # For example, ``tutorontask/templates/ontask/build``
    # will be rendered to ``$(tutor config printroot)/env/plugins/ontask/build``.
    [
        ("ontask/build", "plugins"),
        ("ontask/apps", "plugins"),
    ],
)


########################################
# PATCH LOADING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

# For each file in tutorontask/patches,
# apply a patch based on the file's name and contents.
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutorontask", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))


########################################
# CUSTOM JOBS (a.k.a. "do-commands")
########################################

# A job is a set of tasks, each of which run inside a certain container.
# Jobs are invoked using the `do` command, for example: `tutor local do importdemocourse`.
# A few jobs are built in to Tutor, such as `init` and `createuser`.
# You can also add your own custom jobs:

# To add a custom job, define a Click command that returns a list of tasks,
# where each task is a pair in the form ("<service>", "<shell_command>").
# For example:
### @click.command()
### @click.option("-n", "--name", default="plugin developer")
### def say_hi(name: str) -> list[tuple[str, str]]:
###     """
###     An example job that just prints 'hello' from within both LMS and CMS.
###     """
###     return [
###         ("lms", f"echo 'Hello from LMS, {name}!'"),
###         ("cms", f"echo 'Hello from CMS, {name}!'"),
###     ]


# Then, add the command function to CLI_DO_COMMANDS:
## hooks.Filters.CLI_DO_COMMANDS.add_item(say_hi)

# Now, you can run your job like this:
#   $ tutor local do say-hi --name="eduNEXT"


#######################################
# CUSTOM CLI COMMANDS
#######################################

# Your plugin can also add custom commands directly to the Tutor CLI.
# These commands are run directly on the user's host computer
# (unlike jobs, which are run in containers).

# To define a command group for your plugin, you would define a Click
# group and then add it to CLI_COMMANDS:


### @click.group()
### def ontask() -> None:
###     pass


### hooks.Filters.CLI_COMMANDS.add_item(ontask)


# Then, you would add subcommands directly to the Click group, for example:


### @ontask.command()
### def example_command() -> None:
###     """
###     This is helptext for an example command.
###     """
###     print("You've run an example command.")


# This would allow you to run:
#   $ tutor ontask example-command
