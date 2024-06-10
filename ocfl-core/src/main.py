import os

from datetime import datetime, timezone
from io import BytesIO

from ocflcore import (
    FileSystemStorage,
    OCFLRepository,
    OCFLObject,
    OCFLVersion,
    StorageRoot,
    StreamDigest,
    TopLevelLayout,
)

root = StorageRoot(TopLevelLayout())

# Setup workspace and root storage:
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(base_path)

storage = FileSystemStorage(os.path.join(base_path, "root"))
workspace_storage = FileSystemStorage(os.path.join(base_path, "workspace"))

# Initialize the repository
repository = OCFLRepository(root, storage, workspace_storage=workspace_storage)
repository.initialize()

example_file = StreamDigest(BytesIO(b"minimal example"))

# Create version
v = OCFLVersion(datetime.now(timezone.utc))
v.files.add("file.txt", example_file.stream, example_file.digest)

# Create the object
o = OCFLObject("12345-abcde")
o.versions.append(v)

repository.add(o)
