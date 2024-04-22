const users = [
    {
        // hacker leader
        public: '0xAef9c71b2d81efF1ddE720f57360e0B36c1C9577',
        private: '24871679ddfa877966230f1ff4dbb93616b452c8a251b0c23e631d1c1e36f97d'
    },
    {
        // hacker right hand man
        public: '0x9a89279AA5Be0F7320ae2f650FCfc4AB9427B783',
        private: '3a1b906d49d4314442d61323a2c5b3a98d02033c20f493db0200e84e9cc23416'
        // sha256( sha256(john) + doe )
    },
    {
        // hacker bot
        public: '0x5B0331ED799637DF524bbFC7943f112fB7354a86',
        private: '96d9632f363564cc3032521409cf22a852f2032eec099ed5967c0d000cec607a'
    },
    {
        public: '0xd5DA4652E012e5629A3491616cC89F4E7339bA05',
        private: 'ae6c79d10f1fd410650790e63186ec108fa106325b52fbd88de21a43540e6f2c'
        // sha256(b'hero')
    }
];

// Transfer ETH from the default address to each imported account
async function transferEth() {
    for (i = 0; i < users.length; i++) {
        var account = users[i];
        var to = account.public;
        web3.personal.importRawKey(account.private, 'lol');

        amount = to === '0x5B0331ED799637DF524bbFC7943f112fB7354a86' ? '110' : '101';

        // Transfer ETH to the target account
        await web3.eth.sendTransaction({
            from: eth.accounts[0],
            to,
            value: web3.toWei(amount, 'ether')
        });

        // unlocked accounts indefinitely
        await web3.personal.unlockAccount(to, 'lol', 0);

    }
}

transferEth()
    .then(() => {
        console.log('ETH transferred successfully');
    })
    .catch((error) => {
        console.error('Failed to transfer ETH:', error);
    });