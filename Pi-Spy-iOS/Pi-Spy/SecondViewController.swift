//
//  SecondViewController.swift
//  Pi-Spy
//
//  Created by 彭铭仕 on 2/23/17.
//  Copyright © 2017 Home Surveillance Inc. All rights reserved.
//

import UIKit

class SecondViewController: UIViewController {
  @IBOutlet weak var StreamingSubView: UIView!
  @IBOutlet weak var statusLabel: UILabel!
  @IBOutlet weak var upperBackground: UIView!

  var testView: UIView!

  override func viewDidLoad() {
    super.viewDidLoad()
    NotificationCenter.default.addObserver(self, selector: #selector(self.statusBarActive), name: NSNotification.Name(rawValue: "Recording Activated"), object: nil)
    NotificationCenter.default.addObserver(self, selector: #selector(self.statusBarDeactive), name: NSNotification.Name(rawValue: "Recording Deactivated"), object: nil)
  }

  @IBAction func snapshotButtonPressed(_ sender: Any) {
    NotificationCenter.default.post(name: NSNotification.Name(rawValue: "snapshotButtonPressed"), object: nil)
    print("Notification sent")
  }

  func statusBarActive(notif: Notification) {
    self.statusLabel.text = "Recording Activated"
    self.statusLabel.backgroundColor = UIColor(red: 75/255, green: 214/255, blue: 98/255, alpha: 1)
    self.upperBackground.backgroundColor = UIColor(red: 75/255, green: 214/255, blue: 98/255, alpha: 1)
  }

  func statusBarDeactive(notif: Notification) {
    self.statusLabel.text = "Recording Deactivated"
    self.statusLabel.backgroundColor = UIColor(red: 255/255, green: 89/255, blue: 60/255, alpha: 1)
    self.upperBackground.backgroundColor = UIColor(red: 255/255, green: 89/255, blue: 60/255, alpha: 1)
  }


}
