function validationSignup(values) {

    console.log(values);
  
    let errors = {};
  
    const usernameRegex = /^[a-zA-Z0-9._-]{3,16}$/;
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    const passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,20}$/;

    if (!values.username) {
        errors.username = 'Username is required';
    } else if (!usernameRegex.test(values.username)) {
        errors.username = 'Username must contain at least 3 characters';
    } else {
        errors.username = '';
    }
    
    if (!values.email) {
      errors.email = 'Email is required';
    } else if (!emailRegex.test(values.email)) {
      errors.email = 'Email is invalid';
    } else {
      errors.email = '';
    }
  
    if (!values.password) {
      errors.password = 'Password is required';
    } else if (!passwordRegex.test(values.password)) {
      errors.password = 'Password must contain at least 6 characters, including UPPER/lowercase and numbers';
    } else {
      errors.password = '';
    }
  
    return errors;
  }
  
  export default validationSignup;  