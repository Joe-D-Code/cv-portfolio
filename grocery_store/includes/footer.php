</body>
<!-- Footer Section -->
<footer class="footer-section">
    <div class="footer-container">
        <div class="footer-row">
            <!-- Company Info -->
            <div class="footer-col">
                <h4>Grocery Store</h4>
                <p>Your neighborhood's fresh food destination since 1985.</p>
                <div class="social-links">
                    <a href="#"><i class="fa fa-facebook"></i></a>
                    <a href="#"><i class="fa fa-twitter"></i></a>
                    <a href="#"><i class="fa fa-instagram"></i></a>
                </div>
            </div>

            <!-- Quick Links -->
            <div class="footer-col">
                <h4>Shop With Us</h4>
                <ul>
                    <li><a href="weekly-specials.php">Weekly Specials</a></li>
                    <li><a href="recipes.php">Recipes</a></li>
                    <li><a href="loyalty-program.php">Loyalty Program</a></li>
                    <li><a href="gift-cards.php">Gift Cards</a></li>
                </ul>
            </div>

            <!-- Customer Service -->
            <div class="footer-col">
                <h4>Customer Service</h4>
                <ul>
                    <li><a href="faq.php">FAQ</a></li>
                    <li><a href="returns-policy.php">Returns Policy</a></li>
                    <li><a href="delivery-info.php">Delivery Information</a></li>
                    <li><a href="contact-us.php">Contact Us</a></li>
                </ul>
            </div>

            <!-- Store Hours & Contact -->
            <div class="footer-col">
                <h4>Visit Us</h4>
                <p>123 Fresh Avenue<br>Anytown, ST 12345</p>
                <p>Phone: (555) 123-4567</p>
                <p>Hours: Mon-Sat 8am-9pm<br>Sunday 9am-7pm</p>
            </div>
        </div>

        <!-- Newsletter Signup -->
        <div class="newsletter-container">
            <h4>Subscribe to our newsletter</h4>
            <form action="subscribe.php" method="post">
                <input type="email" name="email" placeholder="Enter your email" required>
                <button type="submit">Subscribe</button>
            </form>
        </div>

        <!-- Bottom Footer -->
        <div class="bottom-footer">
            <div class="copyright">
                <?php echo '&copy; ' . date('Y') . ' Grocery Store. All Rights Reserved.'; ?>
            </div>
            <div class="footer-links">
                <a href="privacy-policy.php">Privacy Policy</a>
                <a href="terms-of-service.php">Terms of Service</a>
                <a href="accessibility.php">Accessibility</a>
            </div>
        </div>
    </div>
</footer>

</html>