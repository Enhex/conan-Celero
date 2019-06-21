from conans import ConanFile, CMake, tools


class CeleroConan(ConanFile):
    name = "Celero"
    version = "master"
    license = "Apache License Version 2.0"
    url = "https://github.com/DigitalInBlue/Celero-Conan"
    description = "C++ Benchmark Authoring Library/Framework"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        self.run("git clone --single-branch --branch=master --depth=1 https://github.com/DigitalInBlue/Celero.git .")

    def build(self):
        cmake = CMake(self)
        if self.options.shared:
            cmake.definitions["CELERO_COMPILE_DYNAMIC_LIBRARIES"] = "ON"
        else:
            cmake.definitions["CELERO_COMPILE_DYNAMIC_LIBRARIES"] = "OFF"
        cmake.definitions["CELERO_ENABLE_EXPERIMENTS"] = "OFF"
        cmake.definitions["CELERO_ENABLE_FOLDERS"] = "OFF"
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="include")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["celero"]
        if not self.options.shared:
            self.cpp_info.defines += ["CELERO_STATIC"]
        if self.settings.os == "Windows":
            self.cpp_info.defines += ["WIN32"]

