CREATE TABLE `csv_imports` (
	`id` text PRIMARY KEY NOT NULL,
	`file_name` text NOT NULL,
	`imported_at` text NOT NULL,
	`row_count` integer NOT NULL,
	`period_start` text NOT NULL,
	`period_end` text NOT NULL,
	`aggregate_json` text NOT NULL,
	`raw_csv` text NOT NULL
);
