import os
import shutil

from ocfl import Object, Store, VersionMetadata

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_path = os.path.join(base_path, "root")
staging_path = os.path.join(base_path, "staging")

object_store = Store(
    root=os.path.join(base_path, "root"),
    # disposition=None
)

if os.path.isdir(root_path):
    shutil.rmtree(root_path)
    object_store.initialize()

identifier = "000001"
version_metadata = VersionMetadata(
    identifier=identifier, message="Initial", name="ssciolla", address="ssciolla@umich.edu"
)

version_dir = "_".join([identifier, "a"])
version_path = os.path.join(staging_path, version_dir)
source_path = os.path.join(staging_path, identifier)
if os.path.isdir(source_path):
    shutil.rmtree(source_path)
shutil.copytree(version_path, source_path)

target_path = os.path.join(root_path, identifier)

object = Object(identifier=identifier)
object.create(
    srcdir=source_path,
    metadata=version_metadata,
    objdir=target_path
)

object_store.list()
for object_path in object_store.object_paths():
    print(object_path)

for version in ["b", "c", "d"]:
    version_metadata = VersionMetadata(
        identifier=identifier,
        message="next"
    )
    version = "_".join([identifier, version])
    version_path = os.path.join(staging_path, version)

    # Create new source version with the same directory name
    shutil.rmtree(source_path)
    shutil.copytree(version_path, source_path)
    object.update(target_path, source_path, version_metadata)
