CREATE TABLE location (
  location_id int(100) NOT NULL AUTO_INCREMENT,
  location_name varchar(50) DEFAULT NULL,
  PRIMARY KEY (location_id));
  
INSERT INTO Location(location_name) VALUES('mulund');
INSERT INTO Location(location_name) VALUES('ghatkopar');
INSERT INTO Location(location_name) VALUES('vikroli');
  
  
  CREATE TABLE product(
   product_id int(100) AUTO_INCREMENT PRIMARY KEY,
   product_name VARCHAR(50) UNIQUE NOT NULL,
   quantity int NOT NULL
);
INSERT INTO product(product_name,quantity) VALUES('hlr',3),('csr',2),('psp',2);
CREATE TABLE movement(
   movement_id int(100) AUTO_INCREMENT PRIMARY KEY,
   timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    from_loc int(50),
	to_loc int(50),
    product_id int(100),
	FOREIGN KEY(product_id)  REFERENCES product(product_id),
	quantity int NOT NULL
);
INSERT INTO movement(from_loc,to_loc,product_id,quantity) VALUES 
 (1,2,1,2),
(3,1,2,3);
SELECT * FROM movement;
CREATE TABLE location_product (
  product_id integer,
  location_id integer,
  PRIMARY key (location_id, product_id),
  FOREIGN KEY (product_id)
    REFERENCES product (product_id),
  FOREIGN KEY (location_id)
    REFERENCES location (location_id));
						 
		