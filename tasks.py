import os
from pathlib import Path
from os.path import join
from shutil import rmtree, copytree

from invoke import Collection, task
from invocations import checks
from invocations.docs import docs, www, sites, watch_docs
from invocations.packaging.release import ns as release_coll, publish
from invocations.testing import count_errors


# TODO: this screams out for the invoke missing-feature of "I just wrap task X,
# assume its signature by default" (even if that is just **kwargs support)
@task
def test(
    ctx,
    verbose=True,
    color=True,
    capture="sys",
    module=None,
    k=None,
    x=False,
    opts="",
    coverage=False,
    include_slow=False,
    loop_on_fail=False,
):
    """
    Run unit tests via pytest.

    By default, known-slow parts of the suite are SKIPPED unless
    ``--include-slow`` is given. (Note that ``--include-slow`` does not mesh
    well with explicit ``--opts="-m=xxx"`` - if ``-m`` is found in ``--opts``,
    ``--include-slow`` will be ignored!)
    """
    pass


@task
def coverage(ctx, opts=""):
    """
    Execute all tests (normal and slow) with coverage enabled.
    """
    pass
    # NOTE: codecov now handled purely in invocations/orb


@task
def guard(ctx, opts=""):
    """
    Execute all tests and then watch for changes, re-running.
    """
    pass


# Until we stop bundling docs w/ releases. Need to discover use cases first.
# TODO: would be nice to tie this into our own version of build() too, but
# still have publish() use that build()...really need to try out classes!
# TODO 4.0: I'd like to just axe the 'built docs in sdist', none of my other
# projects do it.
@task
def publish_(
    ctx, sdist=True, wheel=True, sign=False, dry_run=False, index=None
):
    """
    Wraps invocations.packaging.publish to add baked-in docs folder.
    """
    pass


# Also have to hack up the newly enhanced all_() so it uses our publish
@task(name="all", default=True)
def all_(c, dry_run=False):
    pass


# TODO: "replace one task with another" needs a better public API, this is
# using unpublished internals & skips all the stuff add_task() does re:
# aliasing, defaults etc.
release_coll.tasks["publish"] = publish_
release_coll.tasks["all"] = all_

ns = Collection(
    test,
    coverage,
    guard,
    release_coll,
    docs,
    www,
    watch_docs,
    sites,
    count_errors,
    checks.blacken,
    checks,
)
ns.configure(
    {
        "packaging": {
            # NOTE: many of these are also set in kwarg defaults above; but
            # having them here too means once we get rid of our custom
            # release(), the behavior stays.
            "sign": False,
            "wheel": True,
            "changelog_file": join(
                www.configuration()["sphinx"]["source"], "changelog.rst"
            ),
        },
        "blacken": {"find_opts": r"-and -not -path '*.cci_pycache*'"},
        "docs": {"browse": "remote"},
    }
)
