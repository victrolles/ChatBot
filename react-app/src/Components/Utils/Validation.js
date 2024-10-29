function validationLogin(values) {

  let errors = {};

  const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
  const passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,20}$/;
  
  if (!values.email) {
    errors.email = 'Email is required';
  } else if (!emailRegex.test(values.email)) {
    errors.email = 'Email is invalid';
  }

  if (!values.password) {
    errors.password = 'Password is required';
  } else if (!passwordRegex.test(values.password)) {
    errors.password = 'Password must contain at least 6 characters, including UPPER/lowercase and numbers';
  }
}

export default validationLogin;