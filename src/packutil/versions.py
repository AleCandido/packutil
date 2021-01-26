import pygit2
import semver

main_branch = ["master", "main", "trunk"]
# define release detectors
release_branches = main_branch + ["release", "hotfix"]


def ref_name(ref):
    return "/".join(ref.split("/")[2:])


def get_tags(repo):
    return ["/".join(r.split("/")[2:]) for r in repo.references if "/tags/" in r]


def is_tag_branch(branch_name, prefix="v"):
    if branch_name[0 : len(prefix)] != prefix:
        return False

    try:
        semver.VersionInfo.parse(branch_name[len(prefix) :])
        return True
    except ValueError:
        return False


def mkversion(major, minor, micro):
    return "%d.%d.%d" % (major, minor, micro)


def is_released(repo_path):
    repo = pygit2.Repository(repo_path)

    # determine ids of tagged commits
    tags_commit_sha = [repo.resolve_refish(tag)[0].id for tag in get_tags(repo)]
    return (
        ref_name(repo.head.name) in main_branch or repo.head.target in tags_commit_sha
    )


def write_version_py(major, minor, micro, is_released, filename):
    cnt = """
# THIS FILE IS GENERATED FROM SETUP.PY
major = %(major)d
short_version = '%(short_version)s'
version = '%(version)s'
full_version = '%(full_version)s'
is_released = %(isreleased)s
"""
    version = mkversion(major, minor, micro)
    fullversion = version
    if not is_released:
        fullversion += "-develop"

    with open(filename, "w") as f:
        f.write(
            cnt
            % {
                "major": major,
                "short_version": "%d.%d" % (major, minor),
                "version": version,
                "full_version": fullversion,
                "isreleased": str(is_released),
            }
        )


# =====
# TESTS
# =====


def test_version(repo_path, version_module):
    repo = pygit2.Repository(repo_path)

    tags = get_tags(repo)

    versions = []
    for tag in tags:
        try:
            versions.append(semver.VersionInfo.parse(tag[1:]))
        except ValueError:
            # if tag is not following semver do not append
            pass

    last_version = max(versions)
    assert version_module.major == last_version.major
    assert version_module.short_version == f"{last_version.major}.{last_version.minor}"
    assert version_module.version == str(last_version)
    assert version_module.version == version_module.full_version.split("-")[0]


def test_released(repo_path, version_module):
    repo = pygit2.Repository(repo_path)

    # get repo info
    branch_name = ref_name(repo.head.name)
    full_version = semver.VersionInfo.parse(version_module.full_version)

    # perform checks
    if branch_name.split("/")[0] in release_branches or is_tag_branch(branch_name):
        assert version_module.is_released
        assert full_version.prerelease is None
    else:
        assert not version_module.is_released
        assert full_version.prerelease == "develop"
