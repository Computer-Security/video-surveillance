//
//  ThirdViewController.swift
//  Pi-Spy
//
//  Created by 彭铭仕 on 2/23/17.
//  Copyright © 2017 Home Surveillance Inc. All rights reserved.
//

import UIKit
import Alamofire

class ThirdViewController: UIViewController {
  @IBOutlet weak var activateSwitch: UISwitch!


  override func viewDidLoad() {
    super.viewDidLoad()

    // Do any additional setup after loading the view.
  }

  override func didReceiveMemoryWarning() {
    super.didReceiveMemoryWarning()
    // Dispose of any resources that can be recreated.
  }
  
  @IBAction func switchPressed(_ sender: UISwitch) {
    if (activateSwitch.isOn){
      NSLog("switch on")
      Alamofire.request("http://serverip/activate")
    }else{
      NSLog("switch off")
      Alamofire.request("http://serverip/deactivate")
    }
  }

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
