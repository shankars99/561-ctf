const public_key = '0x3Bf5bB2fC4a4aD7c7b4b2fBc0f7aEe5f4aBfC7f4';
const priv_key =  '24871679ddfa877966230f1ff4dbb93616b452c8a251b0c23e631d1c1e36f97d';


web3.personal.importRawKey(priv_key, 'fhe');

// Transfer ETH to the target account
// await web3.eth.sendTransaction({
//     from: eth.accounts[0],
//     public_key,
//     value: web3.toWei('100', 'ether')
// });

// await web3.personal.unlockAccount(priv_key, 'fhe', 0);

