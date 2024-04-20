const users = [
    {
        // hacker boss
        public: '0xaef9c71b2d81eff1dde720f57360e0b36c1c9577',
        private: '24871679ddfa877966230f1ff4dbb93616b452c8a251b0c23e631d1c1e36f97d'
    },
    {
        // hacker right hand man
        public: '0x9a89279aa5be0f7320ae2f650fcfc4ab9427b783',
        private: '3a1b906d49d4314442d61323a2c5b3a98d02033c20f493db0200e84e9cc23416'
        // sha256( sha256(john) + doe )
    },
    {
        // hacker bot
        public: '0x5b0331ed799637df524bbfc7943f112fb7354a86',
        private: '96d9632f363564cc3032521409cf22a852f2032eec099ed5967c0d000cec607a'
    },
    {
        public: '0xd5da4652e012e5629a3491616cc89f4e7339ba05',
        private: 'ae6c79d10f1fd410650790e63186ec108fa106325b52fbd88de21a43540e6f2c'
        // sha256(b'hero')
    }
];

// Transfer ETH from the default address to each imported account
async function transferEth() {
    for (i = 0; i < users.length; i++) {
        var account = users[i];
        var to = account.public.toLowerCase();
        web3.personal.importRawKey(account.private, 'lol');

        // Transfer ETH to the target account
        await web3.eth.sendTransaction({
            from: eth.accounts[0],
            to,
            value: web3.toWei('100', 'ether')
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