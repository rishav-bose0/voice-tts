class Espeak < Formula
  desc "Text to speech, software speech synthesizer"
  homepage "https://espeak.sourceforge.io/"
  url "https://downloads.sourceforge.net/project/espeak/espeak/espeak-1.48/espeak-1.48.04-source.zip"
  sha256 "bf9a17673adffcc28ff7ea18764f06136547e97bbd9edf2ec612f09b207f0659"
  license all_of: ["GPL-3.0-or-later", "LGPL-2.1-or-later"]
  revision 1

  livecheck do
    url :stable
    regex(%r{url=.*?/espeak[._-]v?(\d+(?:\.\d+)+)(?:-source)?\.(?:t|zip)}i)
  end

  depends_on "portaudio"

  def install
    share.install "espeak-data"
    doc.install Dir["docs/*"]
    cd "src" do
      rm "portaudio.h"
      if OS.mac?
        # macOS does not use -soname so replacing with -install_name to compile for macOS.
        # See https://stackoverflow.com/questions/4580789/ld-unknown-option-soname-on-os-x/32280483#32280483
        inreplace "Makefile", "SONAME_OPT=-Wl,-soname,", "SONAME_OPT=-Wl,-install_name,"
        # macOS does not provide sem_timedwait() so disabling #define USE_ASYNC to compile for macOS.
        # See https://sourceforge.net/p/espeak/discussion/538922/thread/0d957467/#407d
        inreplace "speech.h", "#define USE_ASYNC", "//#define USE_ASYNC"
      end

      system "make", "speak", "DATADIR=#{share}/espeak-data", "PREFIX=#{prefix}"
      bin.install "speak" => "espeak"
      system "make", "libespeak.a", "DATADIR=#{share}/espeak-data", "PREFIX=#{prefix}"
      lib.install "libespeak.a"
      system "make", "libespeak.so", "DATADIR=#{share}/espeak-data", "PREFIX=#{prefix}"
      # macOS does not use the convention libraryname.so.X.Y.Z. macOS uses the convention libraryname.X.dylib
      # See https://stackoverflow.com/questions/4580789/ld-unknown-option-soname-on-os-x/32280483#32280483
      libespeak = shared_library("libespeak", "1.#{version.major_minor}")
      lib.install "libespeak.so.1.#{version.major_minor}" => libespeak
      lib.install_symlink libespeak => shared_library("libespeak", 1)
      lib.install_symlink libespeak => shared_library("libespeak")
      MachO::Tools.change_dylib_id("#{lib}/libespeak.dylib", "#{lib}/libespeak.dylib") if OS.mac?
    end
  end

  test do
    system "#{bin}/espeak", "This is a test for Espeak.", "-w", "out.wav"
  end
end
