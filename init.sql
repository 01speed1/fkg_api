CREATE SEQUENCE IF NOT EXISTS customer_id_seq;
CREATE SEQUENCE IF NOT EXISTS customer_id_seq;
CREATE SEQUENCE IF NOT EXISTS industry_id_seq;
CREATE SEQUENCE IF NOT EXISTS product_id_seq;
CREATE SEQUENCE IF NOT EXISTS report_id_seq;
CREATE SEQUENCE IF NOT EXISTS role_id_seq;
CREATE SEQUENCE IF NOT EXISTS service_id_seq;
CREATE SEQUENCE IF NOT EXISTS supplier_id_seq;
CREATE SEQUENCE IF NOT EXISTS transaction_id_seq;
CREATE SEQUENCE IF NOT EXISTS users_id_seq;
CREATE SEQUENCE IF NOT EXISTS support_cases_id_seq;

CREATE TABLE IF NOT EXISTS Customer (
  id bigint NOT NULL PRIMARY KEY DEFAULT nextval('customer_id_seq'),
  name varchar NOT NULL,
  address varchar,
  industry_id bigint NOT NULL
);

CREATE TABLE IF NOT EXISTS Industry (
  id bigint NOT NULL PRIMARY KEY DEFAULT nextval('industry_id_seq'),
  name varchar NOT NULL
);

CREATE TABLE IF NOT EXISTS Product (
  id bigint NOT NULL PRIMARY KEY DEFAULT nextval('product_id_seq'),
  name varchar
);

CREATE TABLE IF NOT EXISTS Report (
  id bigint NOT NULL PRIMARY KEY DEFAULT nextval('report_id_seq'),
  customer_id bigint,
  service_id bigint,
  start_date date
);

CREATE TABLE IF NOT EXISTS Role (
  id bigint NOT NULL PRIMARY KEY DEFAULT nextval('role_id_seq'),
  name varchar NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Service (
  id bigint NOT NULL PRIMARY KEY DEFAULT nextval('service_id_seq'),
  name varchar NOT NULL
);

CREATE TABLE IF NOT EXISTS Supplier (
  id bigint NOT NULL PRIMARY KEY DEFAULT nextval('supplier_id_seq'),
  name varchar NOT NULL,
  country varchar NOT NULL,
  product_id bigint NOT NULL,
  product_quantity bigint
);

CREATE INDEX IF NOT EXISTS index_1 ON Supplier (id, name);

CREATE TABLE IF NOT EXISTS Transaction (
  id bigint NOT NULL PRIMARY KEY DEFAULT nextval('transaction_id_seq'),
  supplier_id bigint NOT NULL,
  customer_id bigint NOT NULL,
  service_id bigint NOT NULL,
  start_date date NOT NULL,
  mount numeric
);

CREATE TABLE IF NOT EXISTS Users (
  id bigint NOT NULL PRIMARY KEY DEFAULT nextval('users_id_seq'),
  username varchar NOT NULL UNIQUE,
  email varchar NOT NULL UNIQUE,
  hashed_password varchar,
  role_id bigint
);

CREATE TABLE IF NOT EXISTS Support_Cases (
  id bigint NOT NULL PRIMARY KEY DEFAULT nextval('support_cases_id_seq'),
  user_reporter_id bigint,
  status varchar,
  user_support_id bigint,
  details text,
  type varchar,
  title varchar
);

ALTER TABLE Product ADD COLUMN title varchar;


/* ALTER TABLE Customer ADD CONSTRAINT Customer_industry_id_fk FOREIGN KEY (industry_id) REFERENCES Industry (id);
ALTER TABLE Industry ADD CONSTRAINT Industry_customer_id_fk FOREIGN KEY (id) REFERENCES Customer (industry_id);
ALTER TABLE Product ADD CONSTRAINT Product_supplier_id_fk FOREIGN KEY (id) REFERENCES Supplier (product_id);
ALTER TABLE Role ADD CONSTRAINT Role_users_id_fk FOREIGN KEY (id) REFERENCES Users (role_id);
ALTER TABLE Service ADD CONSTRAINT Service_report_id_fk FOREIGN KEY (id) REFERENCES Report (service_id);
ALTER TABLE Transaction ADD CONSTRAINT Transaction_customer_id_fk FOREIGN KEY (customer_id) REFERENCES Customer (id);
ALTER TABLE Transaction ADD CONSTRAINT Transaction_service_id_fk FOREIGN KEY (service_id) REFERENCES Service (id);
ALTER TABLE Transaction ADD CONSTRAINT Transaction_supplier_id_fk FOREIGN KEY (supplier_id) REFERENCES Supplier (id);
ALTER TABLE Users ADD CONSTRAINT Users_support_cases_reporter_fk FOREIGN KEY (id) REFERENCES Support_Cases (user_reporter_id);
ALTER TABLE Users ADD CONSTRAINT Users_support_cases_support_fk FOREIGN KEY (id) REFERENCES Support_Cases (user_support_id);
 */
-- Insert roles
INSERT INTO Role (name) VALUES ('Admin')
ON CONFLICT (name) DO NOTHING;

INSERT INTO Role (name) VALUES ('Support')
ON CONFLICT (name) DO NOTHING;

INSERT INTO Role (name) VALUES ('Developer')
ON CONFLICT (name) DO NOTHING;

INSERT INTO Role (name) VALUES ('Customer')
ON CONFLICT (name) DO NOTHING;

INSERT INTO Role (name) VALUES ('Supplier')
ON CONFLICT (name) DO NOTHING;

-- Insert admin user (hasshed password is 'pass')
INSERT INTO Users (username, email, hashed_password, role_id)
VALUES ('admin', 'admin@example.com', '$2b$12$eI2tIO0aP3zHOAJtKDW/sOiRb8.URqnlxNzhnKjxUSuzweYEyFFkC', (SELECT id FROM Role WHERE name = 'Admin'))
ON CONFLICT (username) DO NOTHING;