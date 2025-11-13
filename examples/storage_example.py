#!/usr/bin/env -S uv run python
"""
Runloop SDK Example - Storage Object Operations

This example demonstrates storage object management:
- Creating storage objects
- Uploading content (text, bytes, files)
- Downloading content
- Mounting storage objects to devboxes
- Storage object lifecycle management
"""

import os
from pathlib import Path

from runloop_api_client import RunloopSDK


def demonstrate_text_upload(sdk: RunloopSDK):
    """Upload text content directly."""
    print("=== Text Content Upload ===")

    content = """Hello from Runloop!
This is a test file created by the SDK.
It contains multiple lines of text.
"""

    obj = sdk.storage_object.upload_from_text(
        content,
        name="test-text-file.txt",
        metadata={"source": "example", "type": "text"},
    )

    print(f"Uploaded text object: {obj.id}")

    # Verify by downloading
    downloaded_text = obj.download_as_text()
    print(f"Downloaded content:\n{downloaded_text}")

    return obj


def demonstrate_bytes_upload(sdk: RunloopSDK):
    """Upload binary content."""
    print("\n=== Binary Content Upload ===")

    # Create some binary data
    binary_data = b"\x89PNG\r\n\x1a\n" + b"Fake PNG header" + b"\x00" * 100

    obj = sdk.storage_object.upload_from_bytes(
        binary_data,
        name="test-binary.bin",
        content_type="binary",
        metadata={"source": "example", "type": "binary"},
    )

    print(f"Uploaded binary object: {obj.id}")
    print(f"Content length: {len(binary_data)} bytes")

    # Verify by downloading
    downloaded_bytes = obj.download_as_bytes()
    print(f"Downloaded {len(downloaded_bytes)} bytes")
    print(f"Content matches: {binary_data == downloaded_bytes}")

    return obj


def demonstrate_file_upload(sdk: RunloopSDK):
    """Upload a file from the filesystem."""
    print("\n=== File Upload ===")

    # Create a temporary file
    temp_file = Path("temp_example_file.txt")
    temp_file.write_text("""This is a file from the filesystem.
It will be uploaded to Runloop storage.
Line 3
Line 4
""")

    try:
        obj = sdk.storage_object.upload_from_file(
            temp_file,
            name="uploaded-file.txt",
            metadata={"source": "filesystem", "original": str(temp_file)},
        )

        print(f"Uploaded file object: {obj.id}")

        # Get object info
        info = obj.refresh()
        print(f"Object name: {info.name}")
        print(f"Content type: {info.content_type}")
        print(f"Metadata: {info.metadata}")

        return obj
    finally:
        # Cleanup temp file
        temp_file.unlink(missing_ok=True)


def demonstrate_manual_upload(sdk: RunloopSDK):
    """Demonstrate manual upload flow with create, upload, complete."""
    print("\n=== Manual Upload Flow ===")

    # Step 1: Create the storage object
    obj = sdk.storage_object.create(
        name="manual-upload.txt",
        content_type="text",
        metadata={"method": "manual"},
    )

    print(f"Created storage object: {obj.id}")
    print(f"Upload URL: {obj.upload_url[:50]}...")

    # Step 2: Upload content to the presigned URL
    content = b"This content was uploaded manually using the upload flow."
    obj.upload_content(content)
    print("Content uploaded to presigned URL")

    # Step 3: Mark the upload as complete
    obj.complete()
    print("Upload marked as complete")

    # Verify
    downloaded = obj.download_as_text()
    print(f"Verified content: {downloaded[:50]}...")

    return obj


def demonstrate_storage_mounting(sdk: RunloopSDK):
    """Mount a storage object to a devbox."""
    print("\n=== Mounting Storage Objects to Devbox ===")

    # Create a storage object with some data
    obj = sdk.storage_object.upload_from_text(
        "This file is mounted in the devbox!\n",
        name="mounted-file.txt",
    )
    print(f"Created storage object: {obj.id}")

    # Create a devbox with the storage object mounted
    devbox = sdk.devbox.create(
        name="storage-mount-devbox",
        mounts=[
            {
                "type": "object_mount",
                "object_id": obj.id,
                "object_path": "/home/user/mounted-data.txt",
            }
        ],
    )

    print(f"Created devbox: {devbox.id}")

    try:
        # Verify the file is accessible in the devbox
        result = devbox.cmd.exec("cat /home/user/mounted-data.txt")
        print(f"Mounted file content: {result.stdout().strip()}")

        # Check file details
        result = devbox.cmd.exec("ls -lh /home/user/mounted-data.txt")
        print(f"File details: {result.stdout().strip()}")

        # Try to use the mounted file
        result = devbox.cmd.exec("wc -l /home/user/mounted-data.txt")
        print(f"Line count: {result.stdout().strip()}")
    finally:
        devbox.shutdown()
        print("Devbox shutdown")

    return obj


def demonstrate_archive_mounting(sdk: RunloopSDK):
    """Create and mount an archive that gets extracted."""
    print("\n=== Mounting Archive (Extraction) ===")

    # Create a temporary directory with files
    import io
    import tarfile

    # Create a tar.gz archive in memory
    tar_buffer = io.BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode="w:gz") as tar:
        # Add some files
        for i in range(3):
            content = f"File {i + 1} content\n".encode()
            info = tarfile.TarInfo(name=f"project/file{i + 1}.txt")
            info.size = len(content)
            tar.addfile(info, io.BytesIO(content))

    tar_data = tar_buffer.getvalue()
    print(f"Created archive with {len(tar_data)} bytes")

    # Upload the archive
    archive_obj = sdk.storage_object.upload_from_bytes(
        tar_data,
        name="project-archive.tar.gz",
        content_type="tar",
    )
    print(f"Uploaded archive: {archive_obj.id}")

    # Create devbox with archive mounted (it will be extracted)
    devbox = sdk.devbox.create(
        name="archive-mount-devbox",
        mounts=[
            {
                "type": "object_mount",
                "object_id": archive_obj.id,
                "object_path": "/home/user/project",
            }
        ],
    )

    print(f"Created devbox: {devbox.id}")

    try:
        # List the extracted contents
        result = devbox.cmd.exec("ls -la /home/user/project/")
        print(f"Extracted archive contents:\n{result.stdout()}")

        # Read one of the files
        result = devbox.cmd.exec("cat /home/user/project/file1.txt")
        print(f"File1 content: {result.stdout().strip()}")
    finally:
        devbox.shutdown()
        print("Devbox shutdown")

    return archive_obj


def list_storage_objects(sdk: RunloopSDK):
    """List all storage objects."""
    print("\n=== Listing Storage Objects ===")

    objects = sdk.storage_object.list(limit=10)

    print(f"Found {len(objects)} storage objects:")
    for obj in objects:
        info = obj.refresh()
        print(f"  - {info.name} ({obj.id}): {info.content_type}")


def cleanup_storage_objects(sdk: RunloopSDK, objects):
    """Delete storage objects to clean up."""
    print("\n=== Cleaning Up Storage Objects ===")

    for obj in objects:
        try:
            info = obj.refresh()
            print(f"Deleting: {info.name} ({obj.id})")
            obj.delete()
            print(f"  Deleted: {obj.id}")
        except Exception as e:
            print(f"  Error deleting {obj.id}: {e}")


def main():
    # Initialize the SDK
    sdk = RunloopSDK()
    print("Initialized Runloop SDK\n")

    created_objects = []

    try:
        # Demonstrate different upload methods
        text_obj = demonstrate_text_upload(sdk)
        created_objects.append(text_obj)

        binary_obj = demonstrate_bytes_upload(sdk)
        created_objects.append(binary_obj)

        file_obj = demonstrate_file_upload(sdk)
        created_objects.append(file_obj)

        manual_obj = demonstrate_manual_upload(sdk)
        created_objects.append(manual_obj)

        # Demonstrate mounting
        mount_obj = demonstrate_storage_mounting(sdk)
        created_objects.append(mount_obj)

        archive_obj = demonstrate_archive_mounting(sdk)
        created_objects.append(archive_obj)

        # List all objects
        list_storage_objects(sdk)

    finally:
        # Cleanup all created objects
        if created_objects:
            cleanup_storage_objects(sdk, created_objects)

    print("\nStorage object example completed!")


if __name__ == "__main__":
    # Ensure API key is set
    if not os.getenv("RUNLOOP_API_KEY"):
        print("Error: RUNLOOP_API_KEY environment variable is not set")
        print("Please set it to your Runloop API key:")
        print("  export RUNLOOP_API_KEY=your-api-key")
        exit(1)

    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        raise
