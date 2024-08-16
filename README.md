# Azure Storage Queue API

This project provides APIs for interacting with Azure Storage Queues using Python and Flask. It includes both producer and consumer APIs with Swagger integration for documentation.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Azure Storage account

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/muntashir-islam/azure-storage-queue.git
    cd azure_queue_api
    ```

2. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Configuration

Update the `AZURE_QUEUE_NAME`, and `AZURE_QUEUE_CONNECTION_STRING` in `app.py` with your Azure Storage account details.

### Running the Application

Start the Flask server:

```bash
python app.py