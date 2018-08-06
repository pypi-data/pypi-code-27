import logging
import os
import sys
from xml.etree import ElementTree

import docker

from build_utils import docker_utils, utils
from build_utils.rules import base_rule

logger = logging.getLogger(__name__)

class BuildMavenArtifact(base_rule.BaseRule):
    def run(self, project_dir):
        # Get project name and version from POM file
        pom_file_path = os.path.join(self.dir_path, project_dir, 'pom.xml')
        pom_tree = ElementTree.parse(pom_file_path)
        pom_ns = {
            'mvn': 'http://maven.apache.org/POM/4.0.0'
        }
        pom_name = pom_tree.find('./mvn:name', pom_ns).text
        pom_version = pom_tree.find('./mvn:version', pom_ns).text

        docker_client = docker.from_env(version='auto')

        artifact_store = self.build_context.get_artifact_store()

        # Build docker context only for calculating content hash
        build_context = docker_utils.create_build_context_archive(project_dir)
        build_context_hash = utils.compute_file_hash(build_context)
        
        artifact_name = "{0}.jar".format(build_context_hash)
        if artifact_store.has_artifact(artifact_name):
            logger.info("Artifact %s already exists in store, skipping...", artifact_name)
            return artifact_store.get_artifact_location(artifact_name)

        bash_script = (
            """
            cp -r /app/src/* /app/work/
            mvn clean install
            """)

        container = docker_client.containers.run(
            image="maven:3.5",
            command="/bin/bash -c '{0}'".format(bash_script),
            detach=True,
            volumes={
                os.path.abspath(project_dir): {
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
            raise RuntimeError("Maven build failed.")

        jar_file_name = '{0}-{1}.jar'.format(pom_name, pom_version)
        tar_stream = container.get_archive(
            posixpath.join('/app/work/target', jar_file_name))[0]
        tar_file_data = read_tar_stream(tar_stream)

        container.remove(v=True)
        
        with tarfile.TarFile(fileobj=tar_file_data) as tar_file:
            jar_file = tar_file.extractfile(jar_file_name)

            return artifact_store.store_artifact_fileobj(
                jar_file,
                artifact_name
            )