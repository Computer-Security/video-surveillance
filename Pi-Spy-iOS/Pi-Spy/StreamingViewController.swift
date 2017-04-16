//
//  StreamingViewController.swift
//  Pi-Spy
//
//  Created by 彭铭仕 on 3/31/17.
//  Copyright © 2017 Home Surveillance Inc. All rights reserved.
//

import UIKit

class StreamingViewController: UIViewController {
  var _mediaplayer : VLCMediaPlayer?

  override func viewDidLoad() {
    super.viewDidLoad()
    NotificationCenter.default.addObserver(self, selector: #selector(self.getSnapshot), name: NSNotification.Name(rawValue: "snapshotButtonPressed"), object: nil)
  }
  
  override func viewDidAppear(_ animated: Bool) {
    _mediaplayer = VLCMediaPlayer()
    _mediaplayer?.drawable = self.view
    let fileURL = NSURL(fileURLWithPath: "/Users/pengmingshi/Desktop/test.mp4")
    _mediaplayer?.media = VLCMedia(url: fileURL as URL!)
  }

  
  @IBAction func viewTapped(_ sender: UITapGestureRecognizer) {
    if (_mediaplayer?.isPlaying)!{
      _mediaplayer?.pause()
    }else{
      _mediaplayer?.play()
    }
  }

  func getSnapshot(notif: Notification){
    print("Notification received.")
    let size = (_mediaplayer?.drawable as AnyObject).frame.size
    UIGraphicsBeginImageContextWithOptions(size, false, UIScreen.main.scale)
    let rec = (_mediaplayer?.drawable as AnyObject).frame
    (_mediaplayer?.drawable as AnyObject).drawHierarchy(in: rec!, afterScreenUpdates: false)
    if let image = UIGraphicsGetImageFromCurrentImageContext(){
      UIImageWriteToSavedPhotosAlbum(image, nil, nil, nil)
    }
    UIGraphicsEndImageContext()
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
