import logging
import os
import sys
from xml.etree import ElementTree

import docker

from build_utils import docker_utils, utils
from build_utils.rules import base_rule

logger = logging.getLogger(__name__)

class BuildGenericArtifact(base_rule.BaseRule):
    def run(self, image, source_dir, build_script_path='build.sh',
            artifact_path='artifact', artifact_suffix=""):
        docker_client = docker.from_env(version='auto')

        artifact_store = self.build_context.get_artifact_store()

        # Build docker context only for calculating content hash
        build_context = docker_utils.create_build_context_archive(source_dir)
        build_context_hash = utils.compute_file_hash(build_context)

        artifact_name = build_context_hash + artifact_suffix
        if artifact_store.has_artifact(artifact_name):
            print "Artifact {0} already exists in store, skipping...".format(artifact_name)
            return artifact_store.get_artifact_location(artifact_name)

        bash_script = (
            """
            cp -r /app/src/* /app/work/
            /bin/bash {0}
            """.format(build_script_path))

        container = docker_client.containers.run(
            image=image,
            command="/bin/bash -c '{0}'".format(bash_script),
            detach=True,
            volumes={
                os.path.abspath(source_dir): {
                    'bind': '/app/src',
                    'mode': 'ro'
                }
            },
            working_dir='/app/work'
        )

        for line in container.logs(stdout=True, stderr=True, stream=True):
            sys.stdout.write(line)

        run_result = container.wait()

        if run_result['StatusCode'] != 0:
            raise RuntimeError("Artifact build failed.")

        tar_stream = container.get_archive(
            posixpath.join('/app/work', artifact_path))[0]
        tar_file_data = read_tar_stream(tar_stream)

        container.remove(v=True)
        
        with tarfile.TarFile(fileobj=tar_file_data) as tar_file:
            artifact_file = tar_file.extractfile(artifact_path)

            return artifact_store.store_artifact_fileobj(
                artifact_file,
                artifact_name
            )
