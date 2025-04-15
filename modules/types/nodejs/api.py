
from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel


class HTTPMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"

class VariableType(str, Enum):
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    OBJECT = "object"
    ARRAY = "array"
    DATE = "date"
    FILE = "file"
    NULL = "null"
    ANY = "any"

class DatabaseTech(str, Enum):
    MONGODB = "mongodb"
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"
    SQLITE = "sqlite"
    REDIS = "redis"
    DYNAMODB = "dynamodb"
    FIREBASE = "firebase"
    NONE = "none"
    OTHER = "other"

class AuthType(str, Enum):
    NONE = "none"
    JWT = "jwt"
    API_KEY = "api_key"
    OAUTH2 = "oauth2"
    BASIC = "basic"
    SESSION = "session"
    OTHER = "other"

class ValidationRule(BaseModel):
    rule_type: str
    value: Any
    message: Optional[str] = None

class Variable(BaseModel):
    name: str
    type: VariableType
    optional: bool = False
    description: Optional[str] = None
    default_value: Optional[Any] = None
    example: Optional[Any] = None
    validation_rules: Optional[List[ValidationRule]] = None
    nested_fields: Optional[List["Variable"]] = None

class Header(BaseModel):
    name: str
    required: bool = False
    description: Optional[str] = None
    example: Optional[str] = None

class API(BaseModel):
    api_name: str
    http_method: HTTPMethod
    route: str
    description: str
    version: Optional[str] = "v1"
    tags: Optional[List[str]] = None
    requires_auth: bool = False
    auth_type: Optional[AuthType] = None
    authorized_roles: Optional[List[str]] = None
    rate_limit: Optional[int] = None
    request_headers: Optional[List[Header]] = None
    request_params: Optional[List[Variable]] = None
    request_body: Optional[List[Variable]] = None
    response_body: Optional[List[Variable]] = None
    response_headers: Optional[List[Header]] = None
    notes: Optional[str] = None

class Project(BaseModel):
    project_name: str
    description: str
    base_route: str = "/api"
    database_tech: DatabaseTech = DatabaseTech.MONGODB
    auth_mechanism: AuthType = AuthType.JWT
    authorization_required: bool = False
    available_roles: Optional[List[str]] = None
    apis: List[API]
    global_headers: Optional[List[Header]] = None
    def to_ai_friendly_description(self) -> str:
        lines = []

        # Project basic info
        lines.append(f"### Project: {self.project_name}")
        lines.append(f"{self.description}\n")

        # Route & database
        lines.append(f"- **Base Route:** `{self.base_route}`")
        lines.append(f"- **Database Technology:** {self.database_tech.value.capitalize()}")

        # Authentication
        if self.authorization_required:
            lines.append(f"- **Authentication Required:** Yes, using `{self.auth_mechanism.value.upper()}`")
            if self.available_roles:
                lines.append(f"- **Available Roles:** {', '.join(self.available_roles)}")
        else:
            lines.append("- **Authentication Required:** No")

        # Global headers
        if self.global_headers:
            lines.append("\n#### Global Headers:")
            for header in self.global_headers:
                header_line = f"- `{header.name}`"
                if header.required:
                    header_line += " (required)"
                if header.description:
                    header_line += f": {header.description}"
                if header.example:
                    header_line += f" (e.g., `{header.example}`)"
                lines.append(header_line)

        # APIs
        lines.append(f"\n### APIs ({len(self.apis)} total):")
        for api in self.apis:
            lines.append(f"\n#### {api.api_name}")
            lines.append(f"- **Method & Route:** `{api.http_method.value}` {api.route}")
            lines.append(f"- **Description:** {api.description}")
            if api.tags:
                lines.append(f"- **Tags:** {', '.join(api.tags)}")
            if api.version:
                lines.append(f"- **Version:** {api.version}")
            if api.requires_auth:
                lines.append(f"- **Requires Auth:** Yes ({api.auth_type.value.upper()})")
                if api.authorized_roles:
                    lines.append(f"  - **Authorized Roles:** {', '.join(api.authorized_roles)}")
            if api.rate_limit:
                lines.append(f"- **Rate Limit:** {api.rate_limit} requests per minute")

            if api.request_headers:
                lines.append(f"- **Request Headers:**")
                for header in api.request_headers:
                    h = f"  - `{header.name}`"
                    if header.required:
                        h += " (required)"
                    if header.description:
                        h += f": {header.description}"
                    if header.example:
                        h += f" (e.g., `{header.example}`)"
                    lines.append(h)

            if api.request_params:
                lines.append(f"- **Query/Path Parameters:**")
                for param in api.request_params:
                    p = f"  - `{param.name}` ({param.type.value})"
                    if param.optional:
                        p += " (optional)"
                    if param.description:
                        p += f": {param.description}"
                    if param.example:
                        p += f" (e.g., `{param.example}`)"
                    lines.append(p)

            if api.request_body:
                lines.append(f"- **Request Body:**")
                for field in api.request_body:
                    b = f"  - `{field.name}` ({field.type.value})"
                    if field.optional:
                        b += " (optional)"
                    if field.description:
                        b += f": {field.description}"
                    if field.example:
                        b += f" (e.g., `{field.example}`)"
                    lines.append(b)

            if api.response_body:
                lines.append(f"- **Response Body:**")
                for field in api.response_body:
                    r = f"  - `{field.name}` ({field.type.value})"
                    if field.description:
                        r += f": {field.description}"
                    if field.example:
                        r += f" (e.g., `{field.example}`)"
                    lines.append(r)

            if api.notes:
                lines.append(f"- **Notes:** {api.notes}")

        return "\n".join(lines)