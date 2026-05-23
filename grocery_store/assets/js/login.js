document.addEventListener('DOMContentLoaded', function() {
    class LoginForm extends React.Component {
        constructor(props) {
            super(props);
            this.state = {
                email: '',
                password: '',
                captcha: '',
                error: null,
                isLoading: false,
                showPassword: false
            };

            // Bind methods
            this.handleSubmit = this.handleSubmit.bind(this);
            this.refreshCaptcha = this.refreshCaptcha.bind(this);
            this.toggleShowPassword = this.toggleShowPassword.bind(this);
        }

        handleSubmit(e) {
            e.preventDefault();
            this.setState({ isLoading: true, error: null });

            fetch('/grocery_store/api/login.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    email: this.state.email,
                    password: this.state.password,
                    captcha: this.state.captcha.toLowerCase()
                }),
                credentials: 'include'
            })
                .then(response => response.json())
                .then(result => {
                    if (result.success) {
                        window.location.href = '/grocery_store/templates/order.php';
                    } else {
                        throw new Error(result.error || 'Login failed');
                    }
                })
                .catch(err => {
                    this.setState({ error: err.message });
                    this.refreshCaptcha();
                })
                .finally(() => {
                    this.setState({ isLoading: false });
                });
        }

        refreshCaptcha() {
            document.getElementById('captcha-image').src =
                '/grocery_store/includes/captcha.php?' + Date.now();
            this.setState({ captcha: '' });
        }

        toggleShowPassword(e) {
            this.setState({ showPassword: e.target.checked });
        }

        render() {
            return (
                <form onSubmit={this.handleSubmit}>
                    {this.state.error && <div className="error-message">{this.state.error}</div>}

                    <input
                        type="email"
                        name="email"
                        value={this.state.email}
                        onChange={(e) => this.setState({ email: e.target.value })}
                        placeholder="Email"
                        required
                    />

                    <input
                        type={this.state.showPassword ? "text" : "password"}
                        name="password"
                        value={this.state.password}
                        onChange={(e) => this.setState({ password: e.target.value })}
                        placeholder="Password"
                        required
                    />

                    <div className="show-password-toggle">
                        <label>
                            <input
                                type="checkbox"
                                checked={this.state.showPassword}
                                onChange={this.toggleShowPassword}
                            />
                            Show Password
                        </label>
                    </div>

                    <div className="captcha">
                        <img
                            src="/grocery_store/includes/captcha.php"
                            alt="CAPTCHA"
                            id="captcha-image"
                            onClick={this.refreshCaptcha}
                            style={{ cursor: 'pointer' }}
                        />
                        <input
                            type="text"
                            name="captcha"
                            value={this.state.captcha}
                            onChange={(e) => this.setState({ captcha: e.target.value })}
                            placeholder="Enter CAPTCHA"
                            required
                        />
                    </div>

                    <button type="submit" disabled={this.state.isLoading}>
                        {this.state.isLoading ? 'Logging in...' : 'Login'}
                    </button>
                </form>
            );
        }
    }


if (container) {
  try {
    const loadingMsg = container.querySelector('.loading-message');
    if (loadingMsg) loadingMsg.remove();
    ReactDOM.render(<LoginForm />, container);
  } catch (e) {
    console.error('Mounting error:', e);
  }
}
});