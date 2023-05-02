import 'dart:io';
import 'package:odoo_rpc/odoo_rpc.dart';

main() async {
  final client = OdooClient('http://localhost:8000');
  try {
    await client.authenticate('001', 'admin', '12345');
    //final sessionInfo = await client.getSessionInfo();
    //final uid = sessionInfo['uid'];
    var res = await client.callKw({
      'model': 'mail.message',
      'method': 'search_read',
      'args': [],
      'kwargs': {
        'context': {'bin_size': true},
        'domain': [
          ['model', '=', 'mail.channel']
        ],
        'fields': ['subject', 'date', 'body', 'write_uid',],
        'limit': 10,
      },
    });
    print('Messages: \n' + res.toString());
  } on OdooException catch (e) {
    print(e);
    client.close();
    exit(-1);
  }
  client.close();
}
