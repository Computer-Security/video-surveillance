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


  /*
  // MARK: - Navigation

  // In a storyboard-based application, you will often want to do a little preparation before navigation
  override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
    // Get the new view controller using segue.destinationViewController.
    // Pass the selected object to the new view controller.
  }
  */

}
