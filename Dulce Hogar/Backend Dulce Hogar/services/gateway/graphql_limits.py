from graphql import GraphQLError
from graphql.language.ast import FieldNode, OperationDefinitionNode
from graphql.validation import ValidationRule


class MaxFieldsRule(ValidationRule):
    MAX_FIELDS = 50

    def enter_operation_definition(
        self,
        node: OperationDefinitionNode,
        *_args
    ) -> None:
        self.field_count = 0
        self.limit_reported = False

    def enter_field(
        self,
        node: FieldNode,
        *_args
    ) -> None:
        self.field_count += 1

        if (
            self.field_count > self.MAX_FIELDS
            and not self.limit_reported
        ):
            self.limit_reported = True

            self.report_error(
                GraphQLError(
                    f"La consulta supera el limite de "
                    f"{self.MAX_FIELDS} campos",
                    [node]
                )
            )