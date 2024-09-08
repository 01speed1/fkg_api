CREATE SEQUENCE IF NOT EXISTS customer_id_seq;
CREATE SEQUENCE IF NOT EXISTS industry_id_seq;
CREATE SEQUENCE IF NOT EXISTS product_id_seq;
CREATE SEQUENCE IF NOT EXISTS report_id_seq;
CREATE SEQUENCE IF NOT EXISTS role_id_seq;
CREATE SEQUENCE IF NOT EXISTS service_id_seq;
CREATE SEQUENCE IF NOT EXISTS supplier_id_seq;
CREATE SEQUENCE IF NOT EXISTS transaction_id_seq;
CREATE SEQUENCE IF NOT EXISTS users_id_seq;
CREATE SEQUENCE IF NOT EXISTS supportcases_id_seq;

CREATE TABLE IF NOT EXISTS Customer (
  id bigint NOT NULL PRIMARY KEY DEFAULT nextval('customer_id_seq'),
  name varchar NOT NULL,
  address varchar,
  industry_id bigint NOT NULL
);

CREATE TABLE IF NOT EXISTS Industry (
  id bigint NOT NULL PRIMARY KEY DEFAULT nextval('industry_id_seq')
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
  name varchar NOT NULL
);

CREATE TABLE IF NOT EXISTS Service (
  id bigint NOT NULL PRIMARY KEY DEFAULT nextval('service_id_seq'),
  name varchar
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
  username varchar NOT NULL,
  hashed_password varchar,
  role_id bigint
);

CREATE TABLE IF NOT EXISTS SupportCases (
  id bigint NOT NULL PRIMARY KEY DEFAULT nextval('supportcases_id_seq'),
  user_reporter_id bigint,
  status bigint,
  user_support_id bigint,
  details bigint
);

/* ALTER TABLE Customer ADD CONSTRAINT Customer_id_fk FOREIGN KEY (industry_id) REFERENCES Industry (id);
ALTER TABLE Industry ADD CONSTRAINT Industry_id_fk FOREIGN KEY (id) REFERENCES Customer (industry_id);
ALTER TABLE Product ADD CONSTRAINT Product_id_fk FOREIGN KEY (product_id) REFERENCES Supplier (id);
ALTER TABLE Role ADD CONSTRAINT Role_id_fk FOREIGN KEY (role_id) REFERENCES Users (id);
ALTER TABLE Service ADD CONSTRAINT Service_id_fk FOREIGN KEY (service_id) REFERENCES Report (id);
ALTER TABLE Transaction ADD CONSTRAINT Transaction_customer_id_fk FOREIGN KEY (customer_id) REFERENCES Customer (id);
ALTER TABLE Transaction ADD CONSTRAINT Transaction_service_id_fk FOREIGN KEY (service_id) REFERENCES Service (id);
ALTER TABLE Transaction ADD CONSTRAINT Transaction_supplier_id_fk FOREIGN KEY (supplier_id) REFERENCES Supplier (id);
ALTER TABLE Users ADD CONSTRAINT Users_user_reporter_id_fk FOREIGN KEY (id) REFERENCES SupportCases (user_reporter_id);
ALTER TABLE Users ADD CONSTRAINT Users_user_support_id_fk FOREIGN KEY (id) REFERENCES SupportCases (user_support_id);
*/