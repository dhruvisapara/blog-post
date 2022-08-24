let blogForm   = document.querySelectorAll(".blog-form")
let container  = document.querySelector("#form-container")
let addButton  = document.querySelector("#add-form")
let totalForms = document.querySelector("#id_form-TOTAL_FORMS")

        let formNum = blogForm.length-1
        addButton.addEventListener('click', addForm)
          var closebtns = document.getElementsByClassName("close");
            var i;
              for (i = 0; i < closebtns.length; i++) {
              closebtns[i].addEventListener("click", function() {
//                     this.parentElement.style.display = 'none';
                       console.log("close button is clicked.")
                       this.parentElement.remove();
              });
        }
        function addForm(e){
            e.preventDefault()
            let newForm = blogForm[0].cloneNode(true)
            let formRegex = RegExp(`form-(\\d){1}-`,'g')
            formNum++
            newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`)
            container.insertBefore(newForm, addButton)
            var closebtns = document.getElementsByClassName("close");
            var i;
              for (i = 0; i < closebtns.length; i++) {
              closebtns[i].addEventListener("click", function() {
                    this.parentElement.style.display = 'none';
                });
        }
            totalForms.setAttribute('value', `${formNum+1}`)
        }
