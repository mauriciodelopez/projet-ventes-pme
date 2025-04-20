-- Chiffre d'affaires total
SELECT SUM(quantity * unit_price) FROM sales;

-- Ventes par produit
SELECT p."Nom", SUM(s.quantity)
FROM sales s
JOIN products p ON s.product_id = p."ID RÃ©fÃ©rence produit"
GROUP BY p."Nom"
ORDER BY 2 DESC;

-- Ventes par ville
SELECT st."Ville", SUM(s.quantity)
FROM sales s
JOIN stores st ON s.store_id = st."ID Magasin"
GROUP BY st."Ville"
ORDER BY 2 DESC;
