import pytest
import tempfile
import os
from PIL import Image
from my_pdf_utils.main import create_pdf_with_images


@pytest.fixture
def image1_png():
    """Create a temporary image1.png file for testing."""
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='red')

    # Create temporary file
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
        img.save(tmp_file.name, 'PNG')
        yield tmp_file.name

    # Cleanup after test
    if os.path.exists(tmp_file.name):
        os.unlink(tmp_file.name)


@pytest.fixture
def multiple_test_images():
    """Create multiple temporary image files for testing."""
    image_files = []
    colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple']

    try:
        for i, color in enumerate(colors):
            img = Image.new('RGB', (100, 100), color=color)
            with tempfile.NamedTemporaryFile(suffix=f'_image{i+1}.png', delete=False) as tmp_file:
                img.save(tmp_file.name, 'PNG')
                image_files.append(tmp_file.name)

        yield image_files
    finally:
        # Cleanup all created files
        for file_path in image_files:
            if os.path.exists(file_path):
                os.unlink(file_path)

def test_create_pdf_with_images(image1_png):
    # Test with valid inputs - using the fixture for actual image files
    image_paths = [image1_png, image1_png, image1_png]  # Use the same image 3 times
    output_path = "test_output.pdf"
    title = "Test PDF"

    # Test the actual function with real image files
    result = create_pdf_with_images(image_paths, output_path, title)

    assert result == output_path

    # Cleanup the generated PDF
    if os.path.exists(output_path):
        os.unlink(output_path)

    # Test with invalid number of images
    try:
        create_pdf_with_images([image1_png] * 13, output_path, title)
    except ValueError as e:
        assert str(e) == "Maximum 12 images allowed"
