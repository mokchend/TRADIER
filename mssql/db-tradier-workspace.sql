select TOP 1 symbol
from bc_stocks_screener bss 
where 
	bss.fg_url is null AND
	bss.fg_is_snapshot = 0 AND
	bss.symbol not like '%.%' AND
	bss.symbol not like '%-%' AND
	bss.fg_processing_status is null

-- RESET All fastgraph snapshot	
UPDATE bc_stocks_screener
 set fg_processing_status = null,
 fg_url = NULL ,
 fg_thumbnail_path = null, 
 fg_is_snapshot = 0

	
-- ================================================================================================
-- Retrieve symbol to be processed by ZennoPoster
-- ================================================================================================

select symbol
from bc_stocks_screener bss 
where bss.fg_url is null and bss.fg_is_snapshot = 0 and bss.symbol not like '%.%'

CREATE TABLE td_orders (
     id INT PRIMARY KEY,
        type VARCHAR(50),
        symbol VARCHAR(50),
        side VARCHAR(50),
        quantity FLOAT,
        status VARCHAR(50),
        duration VARCHAR(50),
        price FLOAT,
        avg_fill_price FLOAT,
        exec_quantity FLOAT,
        last_fill_price FLOAT,
        last_fill_quantity FLOAT,
        remaining_quantity FLOAT,
        create_date DATETIME,
        transaction_date DATETIME,
        class VARCHAR(50),
        num_legs INT,
        strategy VARCHAR(50)
    );

    CREATE TABLE td_legs (
        id INT PRIMARY KEY,
        order_id INT,
        type VARCHAR(50),
        symbol VARCHAR(50),
        side VARCHAR(50),
        quantity FLOAT,
        status VARCHAR(50),
        duration VARCHAR(50),
        price FLOAT,
        avg_fill_price FLOAT,
        exec_quantity FLOAT,
        last_fill_price FLOAT,
        last_fill_quantity FLOAT,
        remaining_quantity FLOAT,
        create_date DATETIME,
        transaction_date DATETIME,
        class VARCHAR(50),
        option_symbol VARCHAR(100),
        FOREIGN KEY (order_id) REFERENCES td_orders(id)
    );

    ALTER TABLE td_position
    ADD is_bc_scraping BIT DEFAULT 0,
        bc_overview_url AS ('https://www.barchart.com/stocks/quotes/' + symbol + '/overview'),
        bc_third_resist_level FLOAT,
        bc_second_resist_level FLOAT,
        bc_first_resist_level FLOAT,
        bc_last_price FLOAT DEFAULT,
        bc_first_support_level FLOAT,
        bc_second_support_level FLOAT,
        bc_third_support_level FLOAT;


CREATE TABLE td_account_order_leg (
    id BIGINT PRIMARY KEY, -- Unique ID for the leg
    order_id BIGINT NOT NULL, -- Foreign key referencing td_account_order
    type VARCHAR(50),
    symbol VARCHAR(50),
    side VARCHAR(50),
    quantity DECIMAL(10, 2),
    status VARCHAR(50),
    duration VARCHAR(50),
    price DECIMAL(10, 2),
    avg_fill_price DECIMAL(10, 2),
    exec_quantity DECIMAL(10, 2),
    last_fill_price DECIMAL(10, 2),
    last_fill_quantity DECIMAL(10, 2),
    remaining_quantity DECIMAL(10, 2),
    create_date DATETIME,
    transaction_date DATETIME,
    class VARCHAR(50),
    option_symbol VARCHAR(100),
    FOREIGN KEY (order_id) REFERENCES td_account_order(id) ON DELETE CASCADE -- Ensures referential integrity
);

 CREATE TABLE td_account_order (
    id BIGINT PRIMARY KEY,
    type VARCHAR(50),
    symbol VARCHAR(50),
    side VARCHAR(50),
    quantity DECIMAL(10, 2),
    status VARCHAR(50),
    duration VARCHAR(50),
    price DECIMAL(10, 2),
    avg_fill_price DECIMAL(10, 2),
    exec_quantity DECIMAL(10, 2),
    last_fill_price DECIMAL(10, 2),
    last_fill_quantity DECIMAL(10, 2),
    remaining_quantity DECIMAL(10, 2),
    create_date DATETIME,
    transaction_date DATETIME,
    class VARCHAR(50),
    strategy VARCHAR(50),
    reason_description TEXT
);

CREATE TABLE stockscreener.dbo.td_position (
	symbol varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	id_position int NOT NULL,
	quantity int NULL,
	cost_basis float NULL,
	date_acquired datetime NULL,
	CONSTRAINT td_position_pk PRIMARY KEY (symbol),
	CONSTRAINT td_position_unique UNIQUE (id_position)
);

    ALTER TABLE td_position
    ADD bc_overview_url AS ('https://www.barchart.com/stocks/quotes/' + symbol + '/overview'),
        bc_third_resist_level FLOAT,
        bc_second_resist_level FLOAT,
        bc_first_resist_level FLOAT,
        bc_last_price FLOAT,
        bc_first_support_level FLOAT,
        bc_second_support_level FLOAT,
        bc_third_support_level FLOAT;

drop table if exists fast_graphs;

CREATE TABLE fast_graphs (
    symbol VARCHAR(50) PRIMARY KEY,
    name VARCHAR(50),
    is_fg_snapshot BIT DEFAULT 0,
    fg_url TEXT,
    fastfacts_previousclose VARCHAR(50),
    fastfacts_blendedpe VARCHAR(50),
    fastfacts_epsyield VARCHAR(50),
    fastfacts_dividendyield VARCHAR(50),
    fastfacts_type VARCHAR(50),
    companyinfo_gicssubindustry VARCHAR(50),
    companyinfo_country VARCHAR(50),
    companyinfo_marketcap VARCHAR(50),
    companyinfo_spcreditrating VARCHAR(50),
    companyinfo_ltdebttocapital VARCHAR(50),
    companyinfo_tev VARCHAR(50),
    graphkey_adjustedoperatingearningsgrowthrate VARCHAR(50),
    graphkey_fairvalueratio VARCHAR(50),
    graphkey_normalperatio VARCHAR(50),
    graphkey_annotations VARCHAR(50),
    analystscorecard_beatzero_year VARCHAR(50),
    analystscorecard_beatone_year VARCHAR(50),
    analystscorecard_hitzero_year VARCHAR(50),
    analystscorecard_hitone_year VARCHAR(50),
    analystscorecard_misszero_year VARCHAR(50),
    analystscorecard_missone_year VARCHAR(50)
);


drop table if exists bc_stocks_screener;
CREATE TABLE bc_stocks_screener (
    symbol VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100),
    create_date DATETIME2 DEFAULT SYSDATETIME(),
    last_update_date DATETIME2 DEFAULT SYSDATETIME(),

    fg_is_snapshot BIT DEFAULT 0,
    fg_url TEXT,
    fg_thumbnail_path TEXT,
    fg_processing_status VARCHAR(50),

    fg_fastfacts_previous_close VARCHAR(50),
    fg_fastfacts_blended_pe VARCHAR(50),
    fg_fastfacts_eps_yield VARCHAR(50),
    fg_fastfacts_dividend_yield VARCHAR(50),
    fg_fastfacts_type VARCHAR(50),
    fg_companyinfo_gics_sub_industry VARCHAR(50),
    fg_companyinfo_country VARCHAR(50),
    fg_companyinfo_marketcap VARCHAR(50),
    fg_companyinfo_sp_credit_rating VARCHAR(50),
    fg_companyinfo_lt_debt_to_capital VARCHAR(50),
    fg_companyinfo_tev VARCHAR(50),
    fg_graphkey_adjusted_operating_earnings_growth_rate VARCHAR(50),
    fg_graphkey_fair_value_ratio VARCHAR(50),
    fg_graphkey_normal_pe_ratio VARCHAR(50),
    fg_graphkey_annotations VARCHAR(50),
    fg_analystscorecard_beat_zero_year VARCHAR(50),
    fg_analystscorecard_beat_one_year VARCHAR(50),
    fg_analystscorecard_hit_zero_year VARCHAR(50),
    fg_analystscorecard_hit_one_year VARCHAR(50),
    fg_analystscorecard_miss_zero_year VARCHAR(50),
    fg_analystscorecard_miss_one_year VARCHAR(50),

    bc_url as ('https://www.barchart.com/stocks/quotes/' + symbol + '/overview'),
    bc_signal VARCHAR(50),
    bc_last DECIMAL(10, 4),
    bc_pivot DECIMAL(10, 4),
    bc_trend VARCHAR(50),
    bc_trend_str VARCHAR(50),
    bc_trend_dir VARCHAR(50),
    bc_opinion VARCHAR(50),
    bc_strength VARCHAR(50),
    bc_direction VARCHAR(50),
    bc_short_term_signal VARCHAR(50),
    bc_med_term_signal VARCHAR(50),
    bc_long_term_signal VARCHAR(50),
    bc_exchange VARCHAR(50),
    bc_industry VARCHAR(100),
    bc_sic_description VARCHAR(255),
    bc_first_res DECIMAL(10, 4),
    bc_second_res DECIMAL(10, 4),
    bc_third_res DECIMAL(10, 4),
    bc_first_sup DECIMAL(10, 4),
    bc_second_sup DECIMAL(10, 4),
    bc_third_sup DECIMAL(10, 4)
);

-- ================================================================================================
-- Add create_date and last_update_date columns to bc_stocks_screener
-- ================================================================================================
ALTER TABLE bc_stocks_screener
ADD create_date DATETIME2 DEFAULT SYSDATETIME(),
    last_update_date DATETIME2 DEFAULT SYSDATETIME();

-- Trigger to auto-update last_update_date
CREATE TRIGGER TRG_UpdateLastUpdateDate
ON bc_stocks_screener
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE bc_stocks_screener
    SET last_update_date = SYSDATETIME()
    FROM bc_stocks_screener t
    INNER JOIN inserted i ON t.symbol = i.symbol;
END;


-- ================================================================================================
-- Provide sql statement for Microsoft SQL Server  to create a table 'td_transation_history' to store transaction history:
-- - It must contains at minima the fields: symbol, quantity, price, created_date, last_modified_date, side, account_name.  
-- - symbol, created_date and account are the composite key. 
-- - created_date and last_modified_date are populated automatically when records are upserted
-- ================================================================================================
drop table if exists td_transaction_history;
CREATE TABLE td_transaction_history (
    created_date DATETIME2 DEFAULT SYSDATETIME() NOT NULL,
    last_modified_date DATETIME2 DEFAULT SYSDATETIME() NOT NULL, 
    account_name NVARCHAR(100) NOT NULL,
    symbol NVARCHAR(50) NOT NULL,
    
    side NVARCHAR(10) NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(18, 2) NOT NULL,
    
    trade_status NVARCHAR(50), -- Optional field : In progress, Completed, Cancelled
    days_since_last_modified AS 
    CASE 
        WHEN status IN ('In progress', 'Completed') THEN DATEDIFF(DAY, created_date, last_modified_date)
        ELSE NULL
    END,


    PRIMARY KEY (symbol, created_date, account_name)
);

-- alter table td_transaction_history
ALTER TABLE td_transaction_history
ADD days_since_last_modified AS 
    CASE 
        WHEN status IN ('In progress', 'Completed') THEN DATEDIFF(DAY, created_date, last_modified_date)
        ELSE NULL
    END;


-- Create a trigger to update the 'last_modified_date' automatically on UPDATE
CREATE TRIGGER trg_UpdateLastModifiedDate
ON td_transaction_history
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE td_transaction_history
    SET last_modified_date = SYSDATETIME()
    FROM td_transaction_history
    INNER JOIN inserted ON 
        td_transaction_history.symbol = inserted.symbol AND
        td_transaction_history.created_date = inserted.created_date AND
        td_transaction_history.account_name = inserted.account_name;
END;
