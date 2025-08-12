import os
import typer
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image

app = typer.Typer()


@app.command()
def create_multi_images(
    image_path: str = typer.Argument(..., help="Path to a PNG image"),
    nb_images: int = typer.Argument(6, help="Number of images to include in the PDF (max 12)"),
    output_path: str = typer.Option("output.pdf", help="Path where to save the PDF file"),
    title: str = typer.Option("Images Grid", help="Title for the PDF document")
) -> str:
    """Creates a PDF A4 with multiple images arranged in a grid.
    """
    typer.echo("Creates a PDF A4 with multiple images arranged in a grid.")
    if nb_images < 1 or nb_images > 12:
        raise ValueError("Number of images must be between 1 and 12")
    image_paths = [image_path] * nb_images
    return create_pdf_with_images(image_paths, output_path, title)

def calculate_cols_rows(nb_images: int) -> tuple[int, int]:
    """Calculate the number of columns and rows based on the number of images."""
    if nb_images <= 2:
        return 1, 2  # 1 column, 2 rows
    elif nb_images <= 4:
        return 2, 2  # 2 columns, 2 rows
    elif nb_images <= 6:
        return 2, 3  # 2 columns, 3 rows
    elif nb_images <= 9:
        return 3, 3  # 3 columns, 3 rows
    elif nb_images <= 12:
        return 3, 4  # 3 columns, 4 rows
    else:
        raise ValueError("Maximum 12 images allowed")

def create_pdf_with_images(
    image_paths: list[str],
    output_path: str = "output.pdf",
    title: str = "Images Grid"
) -> str:
    """Creates a PDF A4 with 6 images arranged in 2 columns and 3 rows.

    Args:
        image_paths (List[str]): List of paths to PNG images (max 6).
        output_path (str): Path where to save the PDF file.
        title (str): Title for the PDF document.

    Returns:
        str: Path to the created PDF file.

    Raises:
        ValueError: If more than 6 images are provided or if image files don't exist.
    """
    if len(image_paths) > 12:
        raise ValueError("Maximum 12 images allowed")

    # Verify all image files exist
    for img_path in image_paths:
        if not os.path.exists(img_path):
            raise ValueError(f"Image file not found: {img_path}")

    # Verify output path is valid
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        raise ValueError(f"Invalid output directory: {output_dir}")

    # A4 dimensions in points (1 point = 1/72 inch)
    page_width, page_height = A4

    # Margins
    margin = 20
    spacing = 20  # Spacing between images

    # Calculate image dimensions
    available_width = page_width - (2 * margin)
    available_height = page_height - (2 * margin)

    # Grid: 3 columns, 4 rows
    cols, rows = calculate_cols_rows(len(image_paths))
    img_width = available_width / cols - spacing
    img_height = available_height / rows - spacing

    # Create PDF
    c = canvas.Canvas(output_path, pagesize=A4)
    c.setTitle(title)

    # Add images to grid
    for i, img_path in enumerate(image_paths):
        # Calculate position
        col = i % cols
        row = i // cols

        x = margin + col * (img_width + spacing)
        y = page_height - margin - (row + 1) * (img_height + spacing)

        # Load and resize image while maintaining aspect ratio
        try:
            with Image.open(img_path) as pil_img:
                # Convert to RGB if necessary (for PNG with transparency)
                if pil_img.mode in ("RGBA", "LA", "P"):
                    pil_img = pil_img.convert("RGB")

                # Calculate scaling to fit within the allocated space
                img_ratio = pil_img.width / pil_img.height
                target_ratio = img_width / img_height

                if img_ratio > target_ratio:
                    # Image is wider than target ratio
                    scaled_width = img_width
                    scaled_height = img_width / img_ratio
                else:
                    # Image is taller than target ratio
                    scaled_height = img_height
                    scaled_width = img_height * img_ratio

                # Center the image in its cell
                centered_x = x + (img_width - scaled_width) / 2
                centered_y = y + (img_height - scaled_height) / 2

                # Add image to PDF
                c.drawImage(
                    img_path,
                    centered_x,
                    centered_y,
                    width=scaled_width,
                    height=scaled_height,
                )

        except Exception as e:
            raise ValueError(f"Error processing image {img_path}: {e}") from e

    c.save()
    return output_path
