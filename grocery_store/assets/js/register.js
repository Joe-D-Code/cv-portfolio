/**
 * React Registration Form Component for Grocery Store
 * This file should be saved at: /grocery_store/assets/js/register.js
 * 
 * IMPORTANT: This file should be processed by Babel or served with type="text/babel"
 * to handle the JSX syntax correctly.
 */

(function () {
  function checkDependencies() {
    if (
      typeof React !== 'undefined' &&
      typeof ReactDOM !== 'undefined' &&
      document.getElementById('register-form')
    ) {
      initializeRegisterForm();
    } else {
      setTimeout(checkDependencies, 50);
    }
  }

  function initializeRegisterForm() {
    class RegisterForm extends React.Component {
      constructor(props) {
        super(props);

        this.state = {
          name: '',
          phone: '',
          email: '',
          password: '',
          showPassword: false,
          formErrors: {},
          isSubmitting: false,
          success: false
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.toggleShowPassword = this.toggleShowPassword.bind(this);
      }

      validateField(name, value) {
        let error = '';
        switch (name) {
          case 'name':
            if (!/^[A-Za-z ]+$/.test(value)) error = "Only letters and spaces allowed";
            break;
          case 'phone':
            if (!/^\d{10}$/.test(value)) error = "10-digit number required";
            break;
          case 'email':
            if (!/\S+@\S+\.\S+/.test(value)) error = "Invalid email format";
            break;
          case 'password':
            if (value.length < 8) error = "Password must be at least 8 characters";
            break;
          default: break;
        }
        return error;
      }

      handleChange(e) {
        const { name, value } = e.target;
        let processedValue = value;

        if (name === 'phone') processedValue = value.replace(/\D/g, '');
        if (name === 'name') processedValue = value.replace(/[^A-Za-z ]/g, '');

        const error = this.validateField(name, processedValue);
        this.setState(prevState => ({
          [name]: processedValue,
          formErrors: { ...prevState.formErrors, [name]: error }
        }));
      }

      toggleShowPassword() {
        this.setState(prevState => ({ showPassword: !prevState.showPassword }));
      }

      async handleSubmit(event) {
        event.preventDefault();
        const { name, phone, email, password } = this.state;

        if (Object.values(this.state.formErrors).every(x => x === '')) {
          this.setState({ isSubmitting: true });
          try {
            const response = await fetch('/grocery_store/api/register.php', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ name, phone, email, password })
            });

            const result = await response.json();
            if (result.success) {
              window.location.href = '/grocery_store/templates/index.php';
            } else {
              this.setState({ formErrors: { form: result.error }, isSubmitting: false });
            }
          } catch (error) {
            this.setState({
              formErrors: { form: 'Registration failed. Please try again.' },
              isSubmitting: false
            });
          }
        }
      }

      render() {
        const { formErrors, isSubmitting, showPassword } = this.state;

        return (
          <form onSubmit={this.handleSubmit} className="registration-form">
            {formErrors.form && <div className="alert alert-error">{formErrors.form}</div>}

            <div className="form-group">
              <label>Full Name:</label>
              <input
                type="text"
                name="name"
                value={this.state.name}
                onChange={this.handleChange}
                className={formErrors.name ? 'input-error' : ''}
                required
              />
              {formErrors.name && <div className="error-message">{formErrors.name}</div>}
            </div>

            <div className="form-group">
              <label>Phone Number:</label>
              <input
                type="tel"
                name="phone"
                value={this.state.phone}
                onChange={this.handleChange}
                className={formErrors.phone ? 'input-error' : ''}
                placeholder="10-digit number"
                required
              />
              {formErrors.phone && <div className="error-message">{formErrors.phone}</div>}
            </div>

            <div className="form-group">
              <label>Email:</label>
              <input
                type="email"
                name="email"
                value={this.state.email}
                onChange={this.handleChange}
                className={formErrors.email ? 'input-error' : ''}
                required
              />
              {formErrors.email && <div className="error-message">{formErrors.email}</div>}
            </div>

            <div className="form-group">
              <label>Password:</label>
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                value={this.state.password}
                onChange={this.handleChange}
                className={formErrors.password ? 'input-error' : ''}
                placeholder="Minimum 8 characters"
                required
              />
              {formErrors.password && <div className="error-message">{formErrors.password}</div>}
            </div>

            <div className="show-password-toggle">
              <label htmlFor="show-password-checkbox">
                Show Password:
              </label>
              <input
                type="checkbox"
                id="show-password-checkbox"
                checked={showPassword}
                onChange={this.toggleShowPassword}
              />
            </div>


            <button
              type="submit"
              className="btn-primary"
              disabled={isSubmitting || Object.values(this.state.formErrors).some(x => x)}
            >
              {isSubmitting ? 'Registering...' : 'Register'}
            </button>
          </form>
        );
      }
    }

    const container = document.getElementById('register-form');
    if (container) {
      const loadingMsg = container.querySelector('.loading-message');
      if (loadingMsg) loadingMsg.remove();
      ReactDOM.render(<RegisterForm />, container);
    }
  }

  checkDependencies();
})();