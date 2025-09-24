import os
import typer
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from PIL import Image
import pymupdf
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

def calculate_cols_rows(nb_images: int) -> tuple[int, int, str]:
    """Calculate the number of columns and rows based on the number of images."""
    if nb_images <= 2:
        return 2, 1, "landscape"  # 1 column, 2 rows
    elif nb_images <= 4:
        return 2, 2, "portrait"  # 2 columns, 2 rows
    elif nb_images <= 6:
        return 3, 2, "landscape"  # 3 columns, 2 rows
    elif nb_images <= 9:
        return 3, 3, "portrait"  # 3 columns, 3 rows
    elif nb_images <= 12:
        return 4, 3, "landscape"  # 4 columns, 3 rows
    else:
        raise ValueError("Maximum 12 images allowed")

def create_pdf_with_images(
    image_paths: list[str],
    output_path: str = "output.pdf",
    title: str = "Images Grid",
    orientation: str = "portrait",
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

    # Grid: 3 columns, 4 rows
    cols, rows, orientation = calculate_cols_rows(len(image_paths))

    # A4 dimensions in points (1 point = 1/72 inch)
    if orientation == "landscape":
        page_width, page_height = landscape(A4)
    else:
        page_width, page_height = A4

    # Margins
    margin = 20
    spacing = 20  # Spacing between images

    # Calculate image dimensions
    available_width = page_width - (2 * margin)
    available_height = page_height - (2 * margin)

    img_width = available_width / cols - spacing
    img_height = available_height / rows - spacing

    # Create PDF
    c = canvas.Canvas(output_path, pagesize=[page_width, page_height])
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


def convert_pdf_to_jpg(    pdf_path: str,
    output_path: str = "output.png",
) -> list[str]:
    """Converts a PDF file to JPG images, one per page.

    Args:
        pdf_path (str): Path to the PDF file to convert.
        output_dir (str): Directory where JPG files will be saved.
        output_prefix (str): Prefix for output JPG filenames.
        dpi (int): DPI for the output images (higher = better quality, larger files).

    Returns:
        list[str]: List of paths to the created JPG files.

    Raises:
        ValueError: If PDF file doesn't exist or output directory is invalid.
    """
    # Check if PDF file exists
    if not os.path.exists(pdf_path):
        raise ValueError(f"PDF file not found: {pdf_path}")
    
    try:
        # Import pdf2image here to give a clear error message if not installed
        doc=pymupdf.open(pdf_path)
        page=doc[0]
        pix = page.get_pixmap()
        pix.save("page-1.png","png",jpg_quality=100)
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        # Save each page as PNG
        output_files = []
        img.save(output_path, "PNG")
        output_files.append(output_path)

        return output_files
    
    except Exception as e:
        raise ValueError(f"Error converting PDF to JPG: {e}") from e


@app.command()
def pdf_to_jpg(
    pdf_path: str = typer.Argument(..., help="Path to the PDF file to convert"),
    output_path: str = typer.Option("output.png", help="Path where the output PNG file will be saved")
) -> None:
    """Converts a PDF file to JPG images, one per page.
    """
    typer.echo(f"Converting PDF '{pdf_path}' to JPG images...")
    
    try:
        output_files = convert_pdf_to_jpg(pdf_path, output_path)
        
        typer.echo(f"✅ Successfully converted {len(output_files)} pages:")
        for output_file in output_files:
            typer.echo(f"   - {output_file}")
        
    except ValueError as e:
        typer.echo(f"❌ Error: {e}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Unexpected error: {e}", err=True)
        raise typer.Exit(1)

