CREATE TABLE `daily_project_metrics` (
	`snapshot_date` text NOT NULL,
	`project_id` text NOT NULL,
	`total_automated_tests` integer NOT NULL,
	`tests_added` integer DEFAULT 0 NOT NULL,
	`total_runs` integer DEFAULT 0 NOT NULL,
	`tests_executed` integer DEFAULT 0 NOT NULL,
	`passed` integer DEFAULT 0 NOT NULL,
	`failed` integer DEFAULT 0 NOT NULL,
	`skipped` integer DEFAULT 0 NOT NULL,
	`errors` integer DEFAULT 0 NOT NULL,
	`pass_rate` real,
	`average_duration_seconds` real,
	PRIMARY KEY(`snapshot_date`, `project_id`),
	FOREIGN KEY (`project_id`) REFERENCES `projects`(`project_id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE TABLE `test_executions` (
	`execution_id` text PRIMARY KEY NOT NULL,
	`project_id` text NOT NULL,
	`execution_name` text,
	`execution_date` text NOT NULL,
	`environment` text,
	`profile` text,
	`suite_name` text,
	`collection_name` text,
	`browser` text,
	`duration_seconds` real,
	`status` text,
	`raw_json` text,
	FOREIGN KEY (`project_id`) REFERENCES `projects`(`project_id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE TABLE `projects` (
	`project_id` text PRIMARY KEY NOT NULL,
	`project_name` text NOT NULL,
	`active` integer DEFAULT 1 NOT NULL,
	`synced_at` text
);
--> statement-breakpoint
CREATE TABLE `test_results` (
	`execution_id` text NOT NULL,
	`test_case_id` text NOT NULL,
	`status` text NOT NULL,
	`duration_seconds` real,
	`failure_category` text DEFAULT 'Unknown' NOT NULL,
	`failure_message` text,
	`raw_json` text,
	PRIMARY KEY(`execution_id`, `test_case_id`),
	FOREIGN KEY (`execution_id`) REFERENCES `test_executions`(`execution_id`) ON UPDATE no action ON DELETE no action,
	FOREIGN KEY (`test_case_id`) REFERENCES `test_cases`(`test_case_id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE TABLE `test_cases` (
	`test_case_id` text PRIMARY KEY NOT NULL,
	`project_id` text NOT NULL,
	`test_case_name` text NOT NULL,
	`created_date` text,
	`updated_date` text,
	`raw_json` text,
	FOREIGN KEY (`project_id`) REFERENCES `projects`(`project_id`) ON UPDATE no action ON DELETE no action
);
