drop table location;
CREATE TABLE location (
  location_id int(100) NOT NULL AUTO_INCREMENT,
  location_name varchar(50) DEFAULT NULL,
  PRIMARY KEY (location_id));
  
INSERT INTO location VALUES (1,'ghatkopar'),(2,'mulund'),(3,'vikhroli'),(4,'kanjur');
  SELECT * FROM location;
  
  CREATE TABLE product(
   product_id int(100) AUTO_INCREMENT PRIMARY KEY,
   product_name VARCHAR(50) UNIQUE NOT NULL 
);
INSERT INTO product(product_name) VALUES('p1'),('p2'),('p3'),('p4'),('p5'),('p6'),('p7');
SELECT * FROM product;
drop table movement;
CREATE TABLE movement(
   movement_id int(100) AUTO_INCREMENT NOT NULL PRIMARY KEY,
   timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    from_loc int(50),
	to_loc int(50),
    product_id int(100) NOT NULL,
    FOREIGN KEY(from_loc)  REFERENCES location(location_id),
    FOREIGN KEY(to_loc)  REFERENCES location(location_id),
	FOREIGN KEY(product_id)  REFERENCES product(product_id),
	quantity int NOT NULL
);
INSERT INTO movement(from_loc,to_loc,product_id,quantity) VALUES(NULL,1,1,5),(NULL,1,1,10),(NULL,1,1,10),(NULL,1,1,10),(NULL,1,5,10),(NULL,4,1,2),(NULL,4,1,1),(NULL,1,5,1),(NULL,4,1,2),(1,NULL,1,5),(1,NULL,5,1),(1,NULL,1,5),(NULL,4,5,1),(4,NULL,5,1),(1,4,1,5),(1,4,5,1),(4,1,5,1),(1,4,1,5),(NULL,1,1,5),(NULL,1,1,1);
SELECT * FROM movement where from_loc=2 ;


SELECT TWO.product_id,product_name,ifnull(TWO.got_quantity,0)-ifnull(ONE.given_quantity,0) as quantity from
(SELECT product_id,sum(m1.quantity) as given_quantity from movement as m1 where from_loc=2  group by product_id) as ONE
RIGHT JOIN
(SELECT product_id,sum(m2.quantity) as got_quantity from movement as m2 where to_loc=2 group by product_id) as TWO
on ONE.product_id=TWO.product_id, Product where Product.product_id = TWO.product_id;    

