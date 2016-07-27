import os
import subprocess
import uranium
from uranium.rules import rule, Once


@uranium.task_requires("install_swagger_ui")
def main(build):
    build.packages.install(".", develop=True)


def test(build):
    if not build.history.get("test_deps"):
        main(build)
        build.packages.install("pytest")
        build.packages.install("pytest-cov")
        build.packages.install("flake8")
        build.history["test_deps"] = True
    build.executables.run([
        "py.test", "--cov", "transmute_core",
        "transmute_core/tests",
        "--cov-report", "term-missing"
    ] + build.options.args)
    # build.executables.run(["flake8", "transmute_core"])


def distribute(build):
    """ distribute the uranium package """
    build.packages.install("wheel")
    build.executables.run([
        "python", "setup.py",
        "sdist", "upload"
    ])


def build_docs(build):
    build.packages.install("sphinx")
    return subprocess.call(
        ["make", "html"], cwd=os.path.join(build.root, "docs")
    )


@rule(Once())
def install_swagger_ui(build):
    import io
    import shutil
    import tarfile
    version = "2.1.4"
    PATH = "https://github.com/swagger-api/swagger-ui/archive/v{0}.tar.gz".format(version)
    TARGET_PATH = os.path.join(build.root, "transmute_core", "swagger", "static")
    EXTRACTED_TOP_LEVEL_DIRNAME = "swagger-ui-{0}".format(version)
    build.packages.install("requests")
    import requests
    r = requests.get(PATH, stream=True)
    stream = io.BytesIO()
    stream.write(r.content)
    stream.seek(0)
    tf = tarfile.TarFile.open(fileobj=stream)
    tf.extractall(path=TARGET_PATH)
    # move the files under the top level directory.
    for name in os.listdir(os.path.join(TARGET_PATH, EXTRACTED_TOP_LEVEL_DIRNAME, "dist")):
        shutil.move(
            os.path.join(TARGET_PATH, EXTRACTED_TOP_LEVEL_DIRNAME, "dist", name),
            TARGET_PATH
        )
