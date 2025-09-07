#!/usr/bin/env python3
"""
Generate Example Tech Blog PDFs for Haystack Q&A Testing
Creates realistic tech blog content as PDFs for testing the Q&A bot.
"""

import os

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def create_pdf_folder():
    """Create the tech_blogs folder if it doesn't exist."""
    folder_path = "./tech_blogs"
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


def create_pdf_document(filename, title, content):
    """Create a PDF document with the given content."""
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "CustomTitle", parent=styles["Heading1"], fontSize=18, spaceAfter=30
    )

    heading_style = ParagraphStyle(
        "CustomHeading", parent=styles["Heading2"], fontSize=14, spaceAfter=12
    )

    body_style = styles["Normal"]
    body_style.fontSize = 11
    body_style.spaceAfter = 12

    # Build the document
    story = []

    # Title
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 12))

    # Process content
    for section in content:
        if section["type"] == "heading":
            story.append(Paragraph(section["text"], heading_style))
        elif section["type"] == "paragraph":
            story.append(Paragraph(section["text"], body_style))
        elif section["type"] == "code":
            code_style = ParagraphStyle(
                "Code", parent=styles["Code"], fontSize=10, leftIndent=20, spaceAfter=12
            )
            story.append(
                Paragraph(f"<font name='Courier'>{section['text']}</font>", code_style)
            )

        story.append(Spacer(1, 6))

    doc.build(story)


def generate_async_python_pdf(folder_path):
    """Generate a PDF about Python async best practices."""
    filename = os.path.join(folder_path, "python_async_best_practices.pdf")
    title = "Python Async Programming: Best Practices and Patterns"

    content = [
        {"type": "heading", "text": "Introduction to Async Programming"},
        {
            "type": "paragraph",
            "text": "Asynchronous programming in Python allows you to write concurrent code that can handle multiple operations without blocking. The async/await syntax, introduced in Python 3.5, provides a clean and intuitive way to work with asynchronous code.",
        },
        {"type": "heading", "text": "Best Practices for Async in Python"},
        {
            "type": "paragraph",
            "text": "Here are the key best practices for writing effective async Python code:",
        },
        {
            "type": "paragraph",
            "text": "<b>1. Use async/await consistently:</b> Always use async def for coroutines and await for calling other async functions. This makes your code more readable and maintainable.",
        },
        {
            "type": "code",
            "text": "async def fetch_data():<br/>    data = await api_call()<br/>    return process(data)",
        },
        {
            "type": "paragraph",
            "text": "<b>2. Avoid blocking calls in async functions:</b> Never use time.sleep() or blocking I/O operations inside async functions. Use asyncio.sleep() and async alternatives instead.",
        },
        {
            "type": "paragraph",
            "text": "<b>3. Use asyncio.gather() for concurrent execution:</b> When you need to run multiple async operations concurrently, use asyncio.gather() to execute them in parallel.",
        },
        {
            "type": "code",
            "text": "results = await asyncio.gather(<br/>    fetch_user(1),<br/>    fetch_user(2),<br/>    fetch_user(3)<br/>)",
        },
        {
            "type": "paragraph",
            "text": "<b>4. Handle exceptions properly:</b> Use try/except blocks around await statements and consider using asyncio.gather(return_exceptions=True) when dealing with multiple operations.",
        },
        {
            "type": "paragraph",
            "text": "<b>5. Use connection pooling:</b> For HTTP requests or database connections, always use connection pools to avoid creating too many connections.",
        },
        {"type": "heading", "text": "Common Pitfalls to Avoid"},
        {
            "type": "paragraph",
            "text": "Avoid these common mistakes when working with async Python:",
        },
        {
            "type": "paragraph",
            "text": "• Don't mix sync and async code without proper handling<br/>• Don't forget to await async functions<br/>• Don't use blocking operations in async functions<br/>• Don't create too many concurrent operations without limits",
        },
        {"type": "heading", "text": "Performance Considerations"},
        {
            "type": "paragraph",
            "text": "Async programming shines in I/O-bound applications but may not provide benefits for CPU-bound tasks. Consider your use case carefully and measure performance to ensure async is the right choice.",
        },
    ]

    create_pdf_document(filename, title, content)
    print(f"Created: {filename}")


def generate_python_performance_pdf(folder_path):
    """Generate a PDF about Python performance optimization."""
    filename = os.path.join(folder_path, "python_performance_optimization.pdf")
    title = "Python Performance Optimization: A Complete Guide"

    content = [
        {"type": "heading", "text": "Understanding Python Performance"},
        {
            "type": "paragraph",
            "text": "Python performance optimization involves understanding bottlenecks, choosing the right data structures, and applying appropriate optimization techniques. This guide covers practical approaches to make your Python code faster.",
        },
        {"type": "heading", "text": "Profiling Your Code"},
        {
            "type": "paragraph",
            "text": "Before optimizing, always profile your code to identify bottlenecks. Use tools like cProfile, line_profiler, and memory_profiler to understand where time is being spent.",
        },
        {"type": "code", "text": "python -m cProfile -s cumulative your_script.py"},
        {"type": "heading", "text": "Data Structure Optimization"},
        {
            "type": "paragraph",
            "text": "Choosing the right data structure can dramatically impact performance. Use sets for membership testing, deque for frequent insertions/deletions at both ends, and dictionaries for fast lookups.",
        },
        {"type": "heading", "text": "Algorithmic Improvements"},
        {
            "type": "paragraph",
            "text": "Often the biggest performance gains come from algorithmic improvements rather than micro-optimizations. Consider time complexity and choose algorithms wisely.",
        },
        {"type": "heading", "text": "Async for I/O-Bound Operations"},
        {
            "type": "paragraph",
            "text": "For I/O-bound operations, async programming can provide significant performance improvements by allowing other operations to proceed while waiting for I/O to complete.",
        },
    ]

    create_pdf_document(filename, title, content)
    print(f"Created: {filename}")


def generate_web_scraping_pdf(folder_path):
    """Generate a PDF about web scraping with Python."""
    filename = os.path.join(folder_path, "python_web_scraping_guide.pdf")
    title = "Modern Web Scraping with Python: Async and Beyond"

    content = [
        {"type": "heading", "text": "Introduction to Web Scraping"},
        {
            "type": "paragraph",
            "text": "Web scraping is the process of extracting data from websites. Modern web scraping often requires handling JavaScript, dealing with rate limits, and managing large-scale data collection efficiently.",
        },
        {"type": "heading", "text": "Async Web Scraping Best Practices"},
        {
            "type": "paragraph",
            "text": "When scraping multiple URLs, async programming can dramatically improve performance. Here are the best practices for async web scraping:",
        },
        {
            "type": "paragraph",
            "text": "<b>Use aiohttp for async HTTP requests:</b> aiohttp is the most popular library for async HTTP operations in Python.",
        },
        {
            "type": "code",
            "text": "async with aiohttp.ClientSession() as session:<br/>    async with session.get(url) as response:<br/>        return await response.text()",
        },
        {
            "type": "paragraph",
            "text": "<b>Implement rate limiting:</b> Use asyncio.Semaphore to limit concurrent requests and avoid overwhelming servers.",
        },
        {
            "type": "code",
            "text": "semaphore = asyncio.Semaphore(10)  # Max 10 concurrent requests<br/>async with semaphore:<br/>    return await fetch_url(url)",
        },
        {
            "type": "paragraph",
            "text": "<b>Handle errors gracefully:</b> Network requests can fail, so implement proper error handling and retry mechanisms.",
        },
        {"type": "heading", "text": "Scaling Web Scraping Operations"},
        {
            "type": "paragraph",
            "text": "For large-scale scraping operations, consider using distributed systems, proxy rotation, and database storage for collected data.",
        },
    ]

    create_pdf_document(filename, title, content)
    print(f"Created: {filename}")


def generate_api_design_pdf(folder_path):
    """Generate a PDF about API design best practices."""
    filename = os.path.join(folder_path, "api_design_best_practices.pdf")
    title = "RESTful API Design: Best Practices for Modern Applications"

    content = [
        {"type": "heading", "text": "Principles of Good API Design"},
        {
            "type": "paragraph",
            "text": "A well-designed API is intuitive, consistent, and follows established conventions. This guide covers the essential principles for creating APIs that developers love to use.",
        },
        {"type": "heading", "text": "RESTful Design Patterns"},
        {
            "type": "paragraph",
            "text": "REST (Representational State Transfer) provides a set of constraints for designing web services. Follow these patterns for consistent API design:",
        },
        {
            "type": "paragraph",
            "text": "• Use HTTP methods correctly (GET, POST, PUT, DELETE)<br/>• Design resource-oriented URLs<br/>• Return appropriate HTTP status codes<br/>• Use consistent naming conventions",
        },
        {"type": "heading", "text": "Async API Considerations"},
        {
            "type": "paragraph",
            "text": "When building APIs with async frameworks like FastAPI or aiohttp, consider these best practices:",
        },
        {
            "type": "paragraph",
            "text": "Use async database drivers and connection pooling to handle concurrent requests efficiently. Implement proper error handling for async operations and consider timeout handling for long-running requests.",
        },
        {"type": "heading", "text": "Performance and Caching"},
        {
            "type": "paragraph",
            "text": "Implement caching strategies, use pagination for large datasets, and consider async processing for heavy operations to maintain good API performance.",
        },
    ]

    create_pdf_document(filename, title, content)
    print(f"Created: {filename}")


def generate_microservices_pdf(folder_path):
    """Generate a PDF about microservices architecture."""
    filename = os.path.join(folder_path, "microservices_architecture_guide.pdf")
    title = "Microservices Architecture: Design Patterns and Best Practices"

    content = [
        {"type": "heading", "text": "Introduction to Microservices"},
        {
            "type": "paragraph",
            "text": "Microservices architecture breaks down applications into small, independent services that communicate over well-defined APIs. This approach offers benefits in scalability, maintainability, and team autonomy.",
        },
        {"type": "heading", "text": "Communication Patterns"},
        {
            "type": "paragraph",
            "text": "Microservices can communicate synchronously via HTTP/REST or asynchronously via message queues. Async communication patterns are often preferred for loose coupling and better resilience.",
        },
        {
            "type": "paragraph",
            "text": "When implementing async communication in Python microservices, use libraries like aio-pika for RabbitMQ or aiokafka for Apache Kafka to handle message passing efficiently.",
        },
        {"type": "heading", "text": "Service Design Best Practices"},
        {
            "type": "paragraph",
            "text": "Design services around business capabilities, ensure each service owns its data, and implement proper monitoring and logging across all services.",
        },
        {"type": "heading", "text": "Async Processing in Microservices"},
        {
            "type": "paragraph",
            "text": "Leverage async processing for handling background tasks, processing queues, and managing long-running operations without blocking the main service threads.",
        },
    ]

    create_pdf_document(filename, title, content)
    print(f"Created: {filename}")


def main():
    """Generate all example PDFs."""
    print("Generating example tech blog PDFs...")

    # Create folder
    folder_path = create_pdf_folder()
    print(f"Created folder: {folder_path}")

    # Generate PDFs
    generate_async_python_pdf(folder_path)
    generate_python_performance_pdf(folder_path)
    generate_web_scraping_pdf(folder_path)
    generate_api_design_pdf(folder_path)
    generate_microservices_pdf(folder_path)

    print(f"\n✅ Generated 5 example PDFs in {folder_path}")
    print("\nThese PDFs contain realistic tech blog content about:")
    print("• Python async best practices")
    print("• Performance optimization")
    print("• Web scraping techniques")
    print("• API design patterns")
    print("• Microservices architecture")
    print("\nYou can now run the Haystack Q&A script!")


if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print("Error: Missing required library.")
        print("Please install reportlab: pip install reportlab")
        print(f"Full error: {e}")
    except Exception as e:
        print(f"Error generating PDFs: {e}")
