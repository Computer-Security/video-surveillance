//
//  ThirdViewController.swift
//  Pi-Spy
//
//  Created by 彭铭仕 on 2/23/17.
//  Copyright © 2017 Home Surveillance Inc. All rights reserved.
//

import UIKit
import Alamofire
import SwiftyJSON
class ThirdViewController: UIViewController {
  @IBOutlet weak var activateSwitch: UISwitch!
  @IBOutlet weak var statusLabel: UILabel!
  @IBOutlet weak var upperBackground: UIView!


  override func viewDidLoad() {
    super.viewDidLoad()
    activateSwitch.isOn = false

    // Do any additional setup after loading the view.
  }

  
  @IBAction func switchPressed(_ sender: UISwitch) {
    if (activateSwitch.isOn){
      NSLog("switch on")
      Alamofire.request("http://66.108.38.161:443/activate").responseJSON { response in
        if let json = response.result.value {
          print("JSON: \(json)")
          if let result = JSON(json)["result"].string {
            if (result=="success"){
              NotificationCenter.default.post(name: NSNotification.Name(rawValue: "Recording Activated"), object: nil)
              self.statusLabel.text = "Recording Activated"
              self.statusLabel.backgroundColor = UIColor(red: 75/255, green: 214/255, blue: 98/255, alpha: 1)
              self.upperBackground.backgroundColor = UIColor(red: 75/255, green: 214/255, blue: 98/255, alpha: 1)
            }
          }
        }
      }
    }else{
      NSLog("switch off")
      Alamofire.request("http://66.108.38.161:443/deactivate").responseJSON { response in

        if let json = response.result.value {
          print("JSON: \(json)")
          if let result = JSON(json)["result"].string {
            if (result=="success"){
              NotificationCenter.default.post(name: NSNotification.Name(rawValue: "Recording Deactivated"), object: nil)
              self.statusLabel.text = "Recording Deactivated"
              self.statusLabel.backgroundColor = UIColor(red: 255/255, green: 89/255, blue: 60/255, alpha: 1)
              self.upperBackground.backgroundColor = UIColor(red: 255/255, green: 89/255, blue: 60/255, alpha: 1)
            }
          }
        }
      }
    }
  }
  
  func changeStatusBar(){
    
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
