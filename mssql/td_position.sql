CREATE TABLE stockscreener.dbo.td_position (
	symbol varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	id_position int NOT NULL,
	quantity int NULL,
	cost_basis float NULL,
	date_acquired datetime NULL,
	CONSTRAINT td_position_pk PRIMARY KEY (symbol),
	CONSTRAINT td_position_unique UNIQUE (id_position)
);