<?php
$db = new mysqli('localhost', 'root', '', 'gruener_faktencheck');
if ($db->connect_error) {
    die("Connection failed: " . $db->connect_error);
}
$db->set_charset("utf8mb4");

$categories_query = "
    SELECT c.*, COUNT(a.id) as article_count 
    FROM categories c
    LEFT JOIN articles a ON c.id = a.category_id
    GROUP BY c.id
    ORDER BY c.name";
$categories = $db->query($categories_query);

$articles_query = "
    SELECT a.*, c.name as category_name 
    FROM articles a
    JOIN categories c ON a.category_id = c.id
    ORDER BY a.published_date DESC
    LIMIT 10";
$articles = $db->query($articles_query);
?>

<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grüner Faktencheck</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">
    <style>
        :root {
            --primary-color: #2E7D32;
            --secondary-color: #4CAF50;
            --light-green: #E8F5E9;
            --dark-green: #1B5E20;
            --gray-100: #f8f9fa;
            --gray-200: #e9ecef;
        }
        body {
            background-color: var(--gray-100);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        .navbar {
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
            padding: 1rem 0;
        }
        .navbar-brand {
            font-weight: 600;
            font-size: 1.4rem;
        }
        .bg-primary-green {
            background-color: var(--primary-color);
        }
        .text-primary-green {
            color: var(--primary-color);
        }
        .section-title {
            position: relative;
            padding-bottom: 1rem;
            margin-bottom: 2rem;
        }
        .section-title::after {
            content: '';
            position: absolute;
            left: 0;
            bottom: 0;
            width: 50px;
            height: 3px;
            background-color: var(--primary-color);
        }
        .section-title.text-center::after {
            left: 50%;
            transform: translateX(-50%);
        }
        .card {
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: none;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.04);
            background: white;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.08);
        }
        .card-title {
            font-size: 1.25rem;
            font-weight: 600;
            line-height: 1.4;
        }
        .card-text {
            color: #6c757d;
            font-size: 0.95rem;
            line-height: 1.6;
        }
        .category-badge {
            background-color: var(--light-green);
            color: var(--dark-green);
            padding: 0.5rem 1.2rem;
            border-radius: 25px;
            text-decoration: none;
            transition: all 0.3s ease;
            font-weight: 500;
            font-size: 0.9rem;
        }
        .category-badge:hover {
            background-color: var(--primary-color);
            color: white;
            transform: translateY(-2px);
        }
        .categories-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        .category-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.04);
        }
        .category-card:hover {
            background: var(--primary-color);
            color: white;
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.08);
        }
        .category-card h5 {
            font-weight: 600;
            margin-bottom: 0.75rem;
        }
        .category-card:hover .badge {
            background: white !important;
            color: var(--primary-color) !important;
        }
        .badge {
            padding: 0.5em 1em;
            font-weight: 500;
        }
        footer {
            background-color: white;
            border-top: 1px solid var(--gray-200);
            padding: 2rem 0;
        }
        .date-badge {
            background-color: var(--gray-100);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.85rem;
            color: #666;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary-green">
        <div class="container">
            <a class="navbar-brand" href="#">
                <i class="bi bi-check-circle-fill"></i> Grüner Faktencheck
            </a>
        </div>
    </nav>

    <div class="container my-5">
        <div class="row mb-5">
            <div class="col-12">
                <h2 class="text-center section-title">
                    <i class="bi bi-tags-fill me-2"></i>Themen & Kategorien
                </h2>
                <div class="categories-grid">
                    <?php while($category = $categories->fetch_assoc()): ?>
                        <a href="#" class="text-decoration-none">
                            <div class="category-card">
                                <h5 class="mb-2"><?php echo htmlspecialchars($category['name']); ?></h5>
                                <span class="badge bg-primary rounded-pill">
                                    <?php echo $category['article_count']; ?> Artikel
                                </span>
                            </div>
                        </a>
                    <?php endwhile; ?>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <h2 class="section-title">Neueste Artikel</h2>
                <div class="row g-4">
                    <?php while($article = $articles->fetch_assoc()): ?>
                        <div class="col-md-6">
                            <div class="card h-100">
                                <div class="card-body p-4">
                                    <h5 class="card-title mb-3">
                                        <a href="<?php echo htmlspecialchars($article['url']); ?>" 
                                           class="text-decoration-none text-dark" 
                                           target="_blank">
                                            <?php echo htmlspecialchars($article['title']); ?>
                                        </a>
                                    </h5>
                                    <p class="card-text mb-4"><?php echo htmlspecialchars($article['description']); ?></p>
                                    <div class="d-flex justify-content-between align-items-center">
                                        <a href="#" class="category-badge">
                                            <i class="bi bi-bookmark-fill me-1"></i>
                                            <?php echo htmlspecialchars($article['category_name']); ?>
                                        </a>
                                        <span class="date-badge">
                                            <i class="bi bi-calendar3 me-1"></i>
                                            <?php echo date('d.m.Y', strtotime($article['published_date'])); ?>
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    <?php endwhile; ?>
                </div>
            </div>
        </div>
    </div>

    <footer class="bg-light py-4 mt-5">
        <div class="container text-center">
            <p class="mb-0">© <?php echo date('Y'); ?> Grüner Faktencheck. Alle Rechte vorbehalten.</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
