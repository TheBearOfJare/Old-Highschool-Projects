function showencryptoptions() {
	x = document.getElementById('encrypt_options');
	x.style.display = "block";
	y = document.getElementById('decrypt_options');
	y.style.display = 'none';
	z = document.getElementById('output')
	z.style.display = 'none'
};

function showdecryptoptions() {
	x = document.getElementById('decrypt_options');
	x.style.display = "block";
	y = document.getElementById('encrypt_options');
	y.style.display = 'none';
	z = document.getElementById('output')
	z.style.display = 'none'
};

function execute() {
	message = document.getElementById('message')
	if (message.value === '') {
		message.value = 'You need to enter some text first'
		return
	}
	
	action = document.getElementById('Encrypt').checked
	
	console.log(action)
	if (action === true) {
		method = document.getElementById('method').value
		encrypt(method)
	}
	else {
		decrypt()
	}
}