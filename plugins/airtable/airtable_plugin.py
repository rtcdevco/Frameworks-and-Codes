"""Airtable Plugin - Main implementation"""

from typing import Dict, Any, List, Optional
from pyairtable import Api
from multi_ai.plugins.base_plugin import BasePlugin, Tool


class AirtablePlugin(BasePlugin):
    """Airtable integration plugin for Multi-AI System"""

    def __init__(self, config: Dict[str, Any]):
        self.api_key = config.get('api_key')
        self.base_id = config.get('base_id')
        self.default_table = config.get('default_table', 'Table 1')
        self.api: Optional[Api] = None
        super().__init__(config)

    async def initialize(self):
        """Initialize Airtable API client"""
        if not self.api_key or not self.base_id:
            raise ValueError("Airtable API key and base ID are required")

        self.api = Api(self.api_key)
        print(f"✓ Airtable plugin initialized for base {self.base_id}")

    async def cleanup(self):
        """Cleanup resources"""
        self.api = None

    def _register_tools(self):
        """Register Airtable tools"""

        # Tool: List Records
        self.tools.append(Tool(
            name="airtable_list_records",
            description="List records from an Airtable table. Supports filtering, sorting, and limiting results.",
            input_schema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the Airtable table"
                    },
                    "max_records": {
                        "type": "integer",
                        "description": "Maximum number of records to return (default: 100)"
                    },
                    "view": {
                        "type": "string",
                        "description": "Name of the view to use"
                    },
                    "formula": {
                        "type": "string",
                        "description": "Airtable formula for filtering (e.g., '{Status} = \"Active\"')"
                    }
                },
                "required": ["table_name"]
            },
            handler=self._list_records
        ))

        # Tool: Create Record
        self.tools.append(Tool(
            name="airtable_create_record",
            description="Create a new record in an Airtable table with specified field values.",
            input_schema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the Airtable table"
                    },
                    "fields": {
                        "type": "object",
                        "description": "Field names and values for the new record"
                    }
                },
                "required": ["table_name", "fields"]
            },
            handler=self._create_record
        ))

        # Tool: Update Record
        self.tools.append(Tool(
            name="airtable_update_record",
            description="Update an existing record in Airtable by record ID.",
            input_schema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the Airtable table"
                    },
                    "record_id": {
                        "type": "string",
                        "description": "Airtable record ID (starts with 'rec')"
                    },
                    "fields": {
                        "type": "object",
                        "description": "Field names and new values"
                    }
                },
                "required": ["table_name", "record_id", "fields"]
            },
            handler=self._update_record
        ))

        # Tool: Delete Record
        self.tools.append(Tool(
            name="airtable_delete_record",
            description="Delete a record from Airtable by record ID.",
            input_schema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the Airtable table"
                    },
                    "record_id": {
                        "type": "string",
                        "description": "Airtable record ID to delete"
                    }
                },
                "required": ["table_name", "record_id"]
            },
            handler=self._delete_record
        ))

        # Tool: Bulk Create
        self.tools.append(Tool(
            name="airtable_bulk_create",
            description="Create multiple records in one operation (max 10 at a time).",
            input_schema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the Airtable table"
                    },
                    "records": {
                        "type": "array",
                        "description": "Array of field objects for each record",
                        "items": {
                            "type": "object"
                        }
                    }
                },
                "required": ["table_name", "records"]
            },
            handler=self._bulk_create
        ))

    async def _list_records(
        self,
        table_name: str,
        max_records: Optional[int] = 100,
        view: Optional[str] = None,
        formula: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List records from a table"""
        table = self.api.table(self.base_id, table_name)

        kwargs = {}
        if max_records:
            kwargs['max_records'] = max_records
        if view:
            kwargs['view'] = view
        if formula:
            kwargs['formula'] = formula

        records = table.all(**kwargs)

        # Format response
        return [{
            "id": record["id"],
            "fields": record["fields"],
            "created_time": record.get("createdTime")
        } for record in records]

    async def _create_record(
        self,
        table_name: str,
        fields: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a single record"""
        table = self.api.table(self.base_id, table_name)
        record = table.create(fields)

        return {
            "id": record["id"],
            "fields": record["fields"],
            "created_time": record.get("createdTime")
        }

    async def _update_record(
        self,
        table_name: str,
        record_id: str,
        fields: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a record"""
        table = self.api.table(self.base_id, table_name)
        record = table.update(record_id, fields)

        return {
            "id": record["id"],
            "fields": record["fields"]
        }

    async def _delete_record(
        self,
        table_name: str,
        record_id: str
    ) -> Dict[str, str]:
        """Delete a record"""
        table = self.api.table(self.base_id, table_name)
        deleted = table.delete(record_id)

        return {
            "id": deleted["id"],
            "deleted": deleted.get("deleted", True)
        }

    async def _bulk_create(
        self,
        table_name: str,
        records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Create multiple records (max 10 at a time)"""
        table = self.api.table(self.base_id, table_name)

        # Airtable API limits bulk operations to 10 records
        batch_size = 10
        all_created = []

        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            created = table.batch_create(batch)
            all_created.extend(created)

        return [{
            "id": record["id"],
            "fields": record["fields"]
        } for record in all_created]
