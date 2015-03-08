var BlockChain = (function() {
    function BlockChain() {
        this.proxy = 'http://104.236.122.118:5000'
        this.api = 'https://blockchain.info/merchant/';
        this.api_code = '6c58b8d9-f429-4af0-a7ae-be98dbeb62f8';
        this.guid = '15200e03-4103-4ce2-ac03-41de26b39183'
        this.address = '19afht1A3Mfkxt69TBnPpWbcT23N8vYmpn';
        this.password = 'password123';

        setInterval(function() {
            console.log(this);
            this.get(this.address);
        }, 60000);
    };
    BlockChain.prototype.send = function(address, amount, note) {
        var params = {
            password: this.password,
            to: address,
            amount: amount,
            from: this.address,
            note: note
        }

        this.request('payment', params, function(response) {
            console.log('payment callback', response);
        });
    };

    BlockChain.prototype.get = function(address) {
        var params = {
            password: this.password,
            address: address,
            confirmations: 0
        }

        this.request('balance', params, function(response) {
            console.log('address_balance callback', response);
            this.balance = response.balance;
            $('#balance').val(this.balance);
        });
    };

    BlockChain.prototype.create = function(password, label) {
        var params = {
            password: password,
            label: label
        }

        this.request('new_address', params, function(response) {
            console.log('new_address callback', response);
            this.address = response.address;
            this.get(this.address);
        });

    };

    BlockChain.prototype.list = function(password) {
        var params = {
            password: password,
	        guid: this.guid
        }
        this.request('list', params, function(response) {
            console.log('addresses callback', response);
            if (response.addresses && response.addresses[0]) {
                console.log(this);
		        this.address = response.addresses[0].address;
		        this.balance = response.addresses[0].balance / 100000000.0;
            }
        });
    }

    BlockChain.prototype.init = function(password, email) {
        var params = {
            password: password,
            email: email,
            label: 'digital swearjar',
            api_code: this.api_code
        }

        this.request('create_wallet', params, function(response) {
            this.guid=response.guid;
            this.address=response.address;
            this.link=response.link;

            this.get(this.address);

        });
    };

    BlockChain.prototype.request = function(action, params, callback) {
        var xhr = new XMLHttpRequest();
        var request = Object.keys(params).map(function(k) { return encodeURIComponent(k) + '=' + encodeURIComponent(params[k]) }).join('&');        

        xhr.open("POST", [this.proxy, action].join('/'), true);
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {

            }
            callback(xhr.responseText);
        }

        console.log(request);
        xhr.send(request);
    };

    return BlockChain;

})();

/* a digital swear jar using bitcoin */
var DigitalSwearJar = (function() {

    function DigitalSwearJar() {
        /* Set up swear jar presets */

        if (!('webkitSpeechRecognition' in window)) {
            alert("Your browser does not support speech recognition");
            return;
        }

        /* Set up blockchain stuff */
        this.blockchain = new BlockChain();

        (function(_this) {
            /* Set up UI event bindings */
            $('#signin').bind('click', function() {
                if ($('#guid').val().length > 0) {
     		    _this.blockchain.guid = $('#guid').val();
                    _this.blockchain.list($('#password').val());
                    console.log('logging in...');
                } else if ($('#email').val().length > 0) {
                    _this.blockchain.init($('#password').val(), $('#email').val());
                    console.log('signing up...');
                } else {
                    alert('Nope! You\'re being dumb.')
                }
            });

            $('#listen').bind('click', function() {
                _this.start();
            });
        })(this);

        $('#youraddress').val(this.blockchain.address);
        $('#jaraddress').val('1ERdaVazk3rBTPTQJibjsSpRvDBpFTVqm');

        /* Set up html 5 webkit speech recognition */
        this.recognition = new webkitSpeechRecognition();
        this.recognition.continuous = true;
        this.recognition.interimResults = true;
        this.recognition.lang = 'en-US';

        /* Speech recognition events and callbacks */
        this.recognition.onstart = function() {
            console.log("Now listening...");
        };
        this.recognition.onerror = function(e) {
            console.log("Error:", e);
        };
        this.recognition.onend = function() {
            console.log("Stopped listening.");
        };

        // Find a way to break down voice into chunks rather than
        // an accumulating string
        (function(_this) {
        _this.recognition.onresult = function(event){

            // This is annoying javascript crap
            if (event.results && event.results[0] && event.results[0][0]) {
                var transcript = event.results[0][0].transcript;
                var confidence = event.results[0][0].confidence;
            }

            // Unavoidable profanity filtering has us matching for the string '***'
            if (transcript.search(/\*+/) > 0 && confidence > 0.75) {
                // event.results[0] is always the highest confidence transcript                
                console.log(_this, transcript.search(/\*+/))
                console.log(event.results[0][0].transcript);    
                _this.stop();
                _this.blockchain.send($('#jaraddress').val(), 80000, 'I was caught saying "'+transcript.match(/.\*+/)+'"!');
                $('#swearModal').modal('show');
                setTimeout(function() {
                    _this.start();
                }, 1000);
            }
            if (event.results && event.results[0] && event.results[0][0])
            console.log(event.results[0][0].confidence, event.results[0][0].transcript);

        };
        })(this);


    }

    DigitalSwearJar.prototype.start = function() {
        this.recognition.start();
    }

    DigitalSwearJar.prototype.stop = function() {
        this.recognition.stop();
    }

    return DigitalSwearJar;
})();

var b = new DigitalSwearJar();
