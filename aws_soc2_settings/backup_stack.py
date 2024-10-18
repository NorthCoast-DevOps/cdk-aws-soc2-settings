"""
This module defines the BackupStack, which sets up backup resources for SOC 2 compliance.
It creates an AWS Backup vault and a backup plan with a daily backup rule. These resources
help ensure data recoverability and availability, which are key aspects of SOC 2 compliance.
The backup plan can be easily extended to include more resources and adjust retention periods.
"""

from aws_cdk import Stack, aws_backup as backup, aws_events as events, Duration
from constructs import Construct

class BackupStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a backup vault
        vault = backup.BackupVault(self, "SOC2BackupVault",
            backup_vault_name="soc2-backup-vault"
        )

        # Create a backup plan
        plan = backup.BackupPlan(self, "SOC2BackupPlan",
            backup_plan_name="soc2-backup-plan"
        )

        # Add a backup rule to the plan
        plan.add_rule(backup.BackupPlanRule(
            backup_vault=vault,
            rule_name="DailyBackup",
            schedule_expression=events.Schedule.cron(
                hour="3",
                minute="0"
            ),
            delete_after=Duration.days(30)
        ))

        # Select resources to backup (you can customize this based on your needs)
        plan.add_selection("SOC2BackupSelection",
            resources=[
                backup.BackupResource.from_tag("backup", "true")
            ]
        )
