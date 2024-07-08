//(function () {
//  "use strict";
//
//  let forms = document.querySelectorAll('.php-email-form');
//
//  forms.forEach(function (e) {
//    e.addEventListener('submit', function (event) {
//      event.preventDefault();
//
//      let thisForm = this;
//
//      let action = thisForm.getAttribute('action');
//      let recaptcha = thisForm.getAttribute('data-recaptcha-site-key');
//
//      if (!action) {
//        console.error('The form action property is not set!');
//        return;
//      }
//      thisForm.querySelector('.loading').classList.add('d-block');
//      thisForm.querySelector('.sent-message').classList.remove('d-block');
//
//      let formData = new FormData(thisForm);
//
//      if (recaptcha) {
//        if (typeof grecaptcha !== "undefined") {
//          grecaptcha.ready(function () {
//            try {
//              grecaptcha.execute(recaptcha, { action: 'php_email_form_submit' })
//                .then(token => {
//                  formData.set('recaptcha-response', token);
//                  php_email_form_submit(thisForm, action, formData);
//                })
//            } catch (error) {
//              console.error(error);
//            }
//          });
//        } else {
//          console.error('The reCaptcha javascript API url is not loaded!')
//        }
//      } else {
//        php_email_form_submit(thisForm, action, formData);
//      }
//    });
//  });
//
//  function php_email_form_submit(thisForm, action, formData) {
//    fetch(action, {
//      method: 'POST',
//      body: formData,
//      headers: { 'X-Requested-With': 'XMLHttpRequest' }
//    })
//      .then(response => {
//        if (response.ok) {
//          return response.text();
//        } else {
//          throw new Error(`${response.status} ${response.statusText} ${response.url}`);
//        }
//      })
//      .then(data => {
//        thisForm.querySelector('.loading').classList.remove('d-block');
//        if (data.trim() == 'OK') {
//          thisForm.querySelector('.sent-message').classList.add('d-block');
//          thisForm.reset();
//        } else {
//          throw new Error(data ? data : 'Form submission failed and no error message returned from: ' + action);
//        }
//      })
//      .catch((error) => {
//        console.error(error);
//      });
//  }
//})();
(function () {
  "use strict";

  let forms = document.querySelectorAll('.php-email-form');

  forms.forEach(function (e) {
    e.addEventListener('submit', function (event) {
      event.preventDefault();

      let thisForm = this;

      let action = thisForm.getAttribute('action');
      let recaptcha = thisForm.getAttribute('data-recaptcha-site-key');

      if (!action) {
        console.error('The form action property is not set!');
        return;
      }
      thisForm.querySelector('.loading').classList.add('d-block'); // Показываем "Loading"
      thisForm.querySelector('.sent-message').style.display = 'none'; // Скрываем сообщение об успешной отправке
      thisForm.querySelector('.error-message').innerHTML = ''; // Очищаем сообщение об ошибке, если оно было отображено ранее

      let formData = new FormData(thisForm);

      if (recaptcha) {
        if (typeof grecaptcha !== "undefined") {
          grecaptcha.ready(function () {
            try {
              grecaptcha.execute(recaptcha, { action: 'php_email_form_submit' })
                .then(token => {
                  formData.set('recaptcha-response', token);
                  php_email_form_submit(thisForm, action, formData);
                })
            } catch (error) {
              console.error(error);
            }
          });
        } else {
          console.error('The reCaptcha javascript API url is not loaded!')
        }
      } else {
        php_email_form_submit(thisForm, action, formData);
      }
    });
  });

  function php_email_form_submit(thisForm, action, formData) {
    fetch(action, {
      method: 'POST',
      body: formData,
      headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
      .then(response => {
        if (response.ok) {
          return response.text();
        } else {
          throw new Error(`${response.status} ${response.statusText} ${response.url}`);
        }
      })
      .then(data => {
        thisForm.querySelector('.loading').classList.remove('d-block'); // Скрываем "Loading"
        if (data.trim() == 'OK') {
          thisForm.querySelector('.sent-message').style.display = 'block'; // Показываем сообщение об успешной отправке
          thisForm.reset();
        } else {
          throw new Error(data ? data : 'Form submission failed and no error message returned from: ' + action);
        }
      })
      .catch((error) => {
        console.error(error);
//        thisForm.querySelector('.error-message').innerHTML = 'Произошла ошибка при отправке формы. Пожалуйста, попробуйте позже.'; // Отображаем сообщение об ошибке
        thisForm.querySelector('.loading').classList.remove('d-block'); // Скрываем "Loading" в случае ошибки
      });
  }
})();
