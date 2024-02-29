START TRANSACTION;
-- you can see that the queries are related to each other by the same user_uuid (first value in the column)

-- admin with no membership
INSERT INTO user_account VALUES ('e3a9dc6e-cad1-11ed-afa1-0242ac120002', 'mich', 'nguyen', 'mich@gmail.com', '02-20-2003', 'NONE', '1');
INSERT INTO user_login VALUES ('e3a9dc6e-cad1-11ed-afa1-0242ac120002', 'ADMIN', 'mich@gmail.com','$2b$12$fpXMLIw1ALlrjxuAJD8xquon54dBCWPmXP5t7WeTRAk9/2eKIo3x2');
-- user with no membership
INSERT INTO user_account VALUES ('e3a9dd72-cad1-11ed-afa1-0242ac120002', 'joe','mom','someone@gmail.com', '02-13-1996', 'NONE', '1');
INSERT INTO user_login VALUES ('e3a9dd72-cad1-11ed-afa1-0242ac120002', 'USER', 'someone@gmail.com','$2b$12$CriXFp4IvckRl4UdaDmadu5UTLiTGG/aYjHXbQJfG.A8r9mqwrcWO');
-- user with silver membership
INSERT INTO user_account VALUES ('6be41a29-8fd3-407e-9b37-784a30492237', 'alex','homer', 'other@gmail.com', '06-13-1998', 'SILVER', '1');
INSERT INTO user_login VALUES ('6be41a29-8fd3-407e-9b37-784a30492237', 'USER', 'other@gmail.com','$2b$12$PFACfUxSzEbglUTMopXx4u1w52RcaJa8zelcqGLdJm5dlMwbR91KK');
-- user with basic membership
INSERT INTO user_account VALUES ('c8304586-5661-4db7-8e75-4dd44b4f7648', 'yves','chu', 'her@gmail.com', '12-11-2002', 'BASIC', '1');
INSERT INTO user_login VALUES ('c8304586-5661-4db7-8e75-4dd44b4f7648', 'USER', 'her@gmail.com','$2b$12$WhzUm6vuWEG/0tDXneCHuuZljGnH.wQcCidwqz0yM9WGbp8cN5sru');

INSERT INTO donation VALUES ('b6cbb3e0-cb79-11ed-afa1-0242ac120002', 'mich@gmail.com', '2023-04-19 05:48:06', 5.05);

-- these are for the report generation of how many of a certain item was sold in a day
/*INSERT INTO exhibitions VALUES ('b6cbb3e0-cb79-11ed-afa1-0242ac120002', '2004-12-13 05:48:06', '5.99','gallery name','Exhibit: Flower', 'some curator', 'an artist');

INSERT INTO exhibitions VALUES ('f91e5c22-cb90-11ed-afa1-0242ac120002', '2013-05-09 02:01:37', '6.99','def name','Exhibit: Painting', 'another curator', 'some artist');

INSERT INTO films VALUES ('d88e557c-cb8e-11ed-afa1-0242ac120002', '2004-12-13 05:48:06', 'Film: Interstellar', '4.99', '124','some director', '5');

*/

COMMIT;
